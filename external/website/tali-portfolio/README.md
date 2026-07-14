# Tali's Portfolio Website 🚀

**Biomedical Engineer & AI/ML Developer Portfolio**

A modern, interactive portfolio website showcasing projects, experience, and technical expertise at the intersection of healthcare technology, artificial intelligence, and innovative engineering.

---

## ✨ Features

- **Hero Section**: Dynamic introduction with animated background elements
- **About Me**: Comprehensive story of the biomedical → AI/ML transition
- **Projects Portfolio**: Filterable showcase (AI/ML, Biomedical, FinTech)
  - Financio (Algorithmic Trading)
  - Apollo Gloves (EMG Gesture Recognition)
  - AI Receptionist Platform
  - Electromagnetic Wristband
  - AI Inventory Management
- **Experience Timeline**: Interactive career journey
- **Philosophy & Vision**: Core principles and future goals
- **AI Chatbot**: Interactive chat interface (ready for backend integration)
  - 🚀 Future: 3D avatar with voice-to-voice capabilities
- **Smooth Navigation**: Scroll-based section highlighting
- **Responsive Design**: Mobile-first approach

---

## 🎨 Tech Stack

- **Frontend**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Future Backend**: Python (Flask/FastAPI) for chatbot

---

## 🎨 Design Philosophy

### Color Palette
- **Biotech Blue** (`#0ea5e9`): Clinical/Medical tech
- **Tech Purple** (`#8b5cf6`): AI/ML capabilities
- **Neural Orange** (`#f97316`): Energy/Innovation
- **Clinical Cyan** (`#06b6d4`): Healthcare precision

### Visual Theme
- Dark mode design (slate-950 base)
- Neural network grid background
- Glassmorphism cards
- Gradient text effects
- Smooth animations

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tali-portfolio
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

---

## 📁 Project Structure

```
tali-portfolio/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx        # Navigation with scroll detection
│   │   ├── Hero.jsx          # Landing section
│   │   ├── About.jsx         # About me section
│   │   ├── Projects.jsx      # Project showcase with filters
│   │   ├── Experience.jsx    # Timeline of experience
│   │   ├── Philosophy.jsx    # Principles and vision
│   │   ├── ChatBot.jsx       # AI chat interface (ready for integration)
│   │   └── Footer.jsx        # Footer with links
│   ├── App.jsx               # Main app component
│   ├── main.jsx              # React entry point
│   └── index.css             # Global styles + Tailwind
├── public/                   # Static assets
├── index.html                # HTML template
├── tailwind.config.js        # Tailwind configuration
├── vite.config.js            # Vite configuration
└── package.json              # Dependencies

```

---

## 🤖 Chatbot Integration (Coming Soon)

The ChatBot component is architected for easy backend integration:

### Frontend Structure
- Message state management
- User input handling
- Typing indicators
- Avatar placeholder for future 3D model

### Backend Integration Points
1. **API Endpoint**: `/api/chat` (POST)
2. **Request Format**: `{ message: string, conversationId?: string }`
3. **Response Format**: `{ reply: string, conversationId: string }`

### Knowledge Base Setup
Use the questions below to populate your chatbot's knowledge base:

#### [Questions provided separately below]

---

## 🎯 Next Steps

### Phase 1: Content Enhancement
- [ ] Add real project links/demos
- [ ] Include resume PDF
- [ ] Add social media links
- [ ] Professional headshot/photos

### Phase 2: Backend Development
- [ ] Set up Flask/FastAPI backend
- [ ] Implement chatbot API
- [ ] Connect knowledge base
- [ ] Deploy backend (Railway/Render)

### Phase 3: Advanced Features
- [ ] 3D avatar integration (Three.js/Ready Player Me)
- [ ] Voice-to-voice chat (Web Speech API + ElevenLabs)
- [ ] Analytics tracking
- [ ] Blog section
- [ ] Project case studies

### Phase 4: Deployment
- [ ] Deploy frontend to Vercel
- [ ] Set up custom domain
- [ ] Configure SSL
- [ ] SEO optimization

---

## 🌐 Deployment

### Vercel (Recommended for Frontend)
1. Push to GitHub
2. Import project in Vercel
3. Deploy automatically

### Netlify Alternative
```bash
npm run build
# Drag and drop `dist/` folder to Netlify
```

---

## 🎨 Customization

### Update Colors
Edit `tailwind.config.js`:
```javascript
colors: {
  'biotech-blue': '#0ea5e9',
  'tech-purple': '#8b5cf6',
  // Add your colors
}
```

### Modify Content
All content is in the component files:
- Personal info: `About.jsx`
- Projects: `Projects.jsx`
- Experience: `Experience.jsx`

---

## 📝 License

MIT License - Feel free to use this template for your own portfolio!

---

## 🤝 Contributing

This is a personal portfolio, but if you find bugs or have suggestions:
1. Open an issue
2. Submit a pull request

---

## 📧 Contact

- **Email**: [your-email]
- **LinkedIn**: [your-linkedin]
- **GitHub**: [your-github]

---

## 💡 Philosophy

> "Carpe Diem" - Seize every moment to build and innovate
> 
> "As You Climb, You Must Lift" - Success is meaningless without mentorship

---

Built with ❤️ using React, Tailwind CSS, and lots of coffee ☕
