# Fine-Tuning Financio's Sentiment Model on Google Cloud — Step by Step

*2026-06-11 · Companion to `Vault of Knowledge/outputs/2026-06-11-finetune-model-analysis.md`*
*Target: Qwen2.5-7B-Instruct QLoRA (primary) + ModernBERT (CPU insurance bet) · Budget: $300 free credits, 90-day window*

---

## Step 0 — Do this BEFORE opening the GCP account

The $300 credit expires 90 days after activation. The dataset takes the longest, so build it first on your Mac. Don't start the clock until Step 2.

**0.1 Export your proprietary data (the moat).** From `~/projects/shared_data/stocks/`, collect per ticker: news headlines/snippets Morgans scored, Reddit post titles+bodies, SEC filing snippets. Target 20-40k texts across your 18 rotation tickers + ~30 sector peers.

**0.2 Annotate with a frontier model** (the annotators-paper recipe):

```
For each text, prompt GPT/Claude with:
  "Label this financial text's sentiment toward {TICKER} as exactly one of
   bearish / neutral / bullish, plus a confidence 0-1.
   Text: {TEXT}
   Reply as JSON: {"label": ..., "confidence": ...}"
```
- Batch via the API (~$30-50 for 30k texts with a small model, e.g. Haiku-class).
- **Spot-check everything with confidence < 0.7 yourself** (expect ~35%). Fix or drop.
- Dedup near-identical headlines (same story syndicated) — leakage source #1.

**0.3 Build the gold eval set:** 1,000 texts you've personally verified, stratified across tickers/sources/labels. **Split by TIME, not randomly** (train ≤ April 2026, eval = May-June 2026) so you measure generalization, not memorization. Save as JSONL:

```json
{"text": "...", "ticker": "NVDA", "source": "newsapi", "label": "bullish"}
```

Files: `train.jsonl`, `eval_gold.jsonl`. Optionally add public sets to training: TFNS (9.5k, HuggingFace `zeroshot/twitter-financial-news-sentiment`). Keep Financial PhraseBank OUT of commercial training (CC BY-NC-SA) — use it as a second eval only.

---

## Step 1 — GCP account & project

1. https://cloud.google.com/free → start free trial ($300/90 days; card required, no auto-charge on expiry).
2. Create project `financio-finetune`. Enable **Compute Engine API**.
3. Install CLI on your Mac: `brew install google-cloud-sdk && gcloud init`.
4. **Request GPU quota** (new accounts start at 0): Console → IAM & Admin → Quotas → filter "GPUs (all regions)" → request **1**. Also "Preemptible NVIDIA L4 GPUs" in your region (us-central1 is usually cheapest/most available). Approval is typically minutes-to-hours for 1 GPU.
5. Create a bucket for spot-safe checkpoints: `gcloud storage buckets create gs://financio-ft-$RANDOM --location=us-central1`

## Step 2 — Launch the training VM (L4 spot ≈ $0.38/hr)

```bash
gcloud compute instances create ft-l4 \
  --zone=us-central1-a \
  --machine-type=g2-standard-8 \
  --provisioning-model=SPOT --instance-termination-action=STOP \
  --image-family=ubuntu-2404-lts-amd64  --image-project=ubuntu-os-cloud \
  --boot-disk-size=200GB \
  --metadata="install-nvidia-driver=True"
```
Notes:
- `g2-standard-8` includes 1× L4 (24GB) — enough for 7B QLoRA.
- **Spot can be preempted.** That's why we checkpoint to GCS every 200 steps; restarting resumes. Savings: ~56% vs on-demand.
- If the image family name has rotated, list current ones: `gcloud compute images list --project deep-learning-platform-release --filter="family~gpu"`.
- SSH in: `gcloud compute ssh ft-l4 --zone=us-central1-a`

## Step 3 — Environment (on the VM)

```bash
pip install -U pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
pip install -U "transformers>=4.44" peft trl "bitsandbytes>=0.44" datasets accelerate evaluate scikit-learn sentencepiece protobuf
# upload your data from the Mac:
#   gcloud compute scp train.jsonl eval_gold.jsonl ft-l4:~ --zone=us-central1-a
```

## Step 4 — Train Qwen2.5-7B QLoRA (rank 8 — the FinLoRA-validated config)

Format each example as a chat turn (`train_chat.jsonl` via a 10-line preprocessing script):

```
user: Classify the sentiment of this financial text toward {ticker} as bearish, neutral, or bullish.\n{text}
assistant: {label}
```

`train_qlora.py` (core of it):

```python
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
import torch

MODEL = "Qwen/Qwen2.5-7B-Instruct"
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=bnb, device_map="auto")
tok = AutoTokenizer.from_pretrained(MODEL)

lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj"])

ds = load_dataset("json", data_files={"train": "train_chat.jsonl"})

cfg = SFTConfig(output_dir="out", num_train_epochs=3, per_device_train_batch_size=4,
                gradient_accumulation_steps=4, learning_rate=2e-4, bf16=True,
                logging_steps=20, save_steps=200, save_total_limit=2,
                lr_scheduler_type="cosine", warmup_ratio=0.03)

SFTTrainer(model=model, args=cfg, train_dataset=ds["train"],
           peft_config=lora, processing_class=tok).train()
```

Run it spot-safely:
```bash
nohup python3 train_qlora.py > train.log 2>&1 &
watch -n 60 'tail -2 train.log; gsutil -m rsync -r out gs://financio-ft-17512/out'  # or a cron rsync
```
Expect **4-8 hours ≈ $2-4**. If preempted: restart VM, `gsutil rsync` the checkpoint back, resume with `trainer.train(resume_from_checkpoint=True)`.

## Step 5 — Train ModernBERT (same data, ~20 min, same VM)

Standard `AutoModelForSequenceClassification` with `answerdotai/ModernBERT-base`, 3 labels, lr 2e-5, 3 epochs, batch 32. This is the cheap insurance bet — it later runs on the VPS **CPU** with no GPU at all.

## Step 6 — Evaluate on the gold set (the judge is the eval, not vibes)

For both models, predict `eval_gold.jsonl`, compute **macro-F1** + per-class F1 + confusion matrix. Also score your current stack (VADER, FinBERT `ProsusAI/finbert`) on the same set as baselines.

**Decision rule (locked in the analysis):** if ModernBERT is within ~2 macro-F1 of the 7B → ship ModernBERT (free CPU inference). Otherwise ship the 7B.

## Step 7 — Export & ship

**Qwen path:** merge + quantize to GGUF:
```bash
python - <<'EOF'
from peft import AutoPeftModelForCausalLM
m = AutoPeftModelForCausalLM.from_pretrained("out/checkpoint-final", torch_dtype="bfloat16")
m.merge_and_unload().save_pretrained("merged")
EOF
git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp
python convert_hf_to_gguf.py ../merged --outfile financio-sent-7b.gguf
./llama-quantize financio-sent-7b.gguf financio-sent-7b-Q4_K_M.gguf Q4_K_M   # ~4.7GB
gsutil cp financio-sent-7b-Q4_K_M.gguf gs://YOUR_BUCKET/
```
Serve with `llama-server` (cloud VM while credits last → local GPU after; a used RTX 3090 runs it at ~87 tok/s). **ModernBERT path:** export ONNX (`optimum-cli export onnx`), copy to the VPS, run under `onnxruntime` — hundreds of texts/sec on CPU.

**Wire into Morgans:** add a scorer module that calls the served model (or ONNX in-process) where FinBERT currently scores; run it **in parallel** with VADER+FinBERT for 2-4 weeks writing to a separate column; compare ensemble backtest IC before switching the live weight. Same lookahead discipline as always: score only texts published before each decision.

## Step 8 — Cost hygiene (don't donate your credits to Google)

- `gcloud compute instances stop ft-l4` **the moment you're not training** — a stopped VM bills only the disk (~$0.01/hr).
- Billing → Budgets & alerts → alert at $50/$150/$250.
- When fully done: delete the VM, keep the bucket (pennies).
- Total expected spend for the whole program incl. 3-5 experiment runs: **$15-40 of the $300.**

## Checklist

- [ ] 0. Dataset built + gold eval set (BEFORE activating credits)
- [ ] 1. GCP project, GPU quota approved, bucket created
- [ ] 2. L4 spot VM up
- [ ] 3. Qwen QLoRA trained (checkpoints in GCS)
- [ ] 4. ModernBERT trained
- [ ] 5. Gold-set eval: both models vs VADER/FinBERT baselines
- [ ] 6. Winner exported (GGUF Q4 or ONNX) and downloaded
- [ ] 7. Parallel A/B in Morgans for 2-4 weeks
- [ ] 8. VM stopped/deleted, budget alerts on
