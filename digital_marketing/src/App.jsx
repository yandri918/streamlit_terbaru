import { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

import Hero from './components/Hero/Hero';
import ABTestingSimulator from './components/ABTesting/ABTestingSimulator';
import FunnelStrategy from './components/Funnel/FunnelStrategy';
import ProgrammaticAds from './components/ProgrammaticAds/ProgrammaticAds';
import DataScienceMMM from './components/DataScience/DataScienceMMM';

// --- Styled Components ---
const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  z-index: 1;
`;

const BackgroundLayers = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  overflow: hidden;
  background-color: var(--bg-dark);

  /* Abstract glow blobs */
  &::before, &::after {
    content: '';
    position: absolute;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    filter: blur(150px);
    opacity: 0.15;
    animation: float 20s ease-in-out infinite alternate;
  }

  &::before {
    top: -200px;
    left: -200px;
    background: var(--primary-neon);
  }

  &::after {
    bottom: -200px;
    right: -200px;
    background: var(--secondary-neon);
    animation-delay: -10s;
  }
`;

const MainContent = styled.main`
  flex: 1;
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 80px 20px 40px; /* Padding for fixed navbar */
`;

const Navbar = styled.nav`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 5%;
  background: rgba(10, 10, 15, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  z-index: 1000;
`;

const NavLogo = styled.div`
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  cursor: pointer;
`;

const NavLinks = styled.div`
  display: flex;
  gap: 2rem;
  
  @media (max-width: 768px) {
    display: none; /* Hide on mobile for now */
  }
`;

const NavLinkBase = styled.a`
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.3s ease;
  cursor: pointer;

  &:hover {
    color: var(--primary-neon);
  }
`;

const Footer = styled.footer`
  width: 100%;
  padding: 40px 5%;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  background: var(--bg-darker);
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
`;

function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <AppContainer>
      <BackgroundLayers />
      
      <Navbar>
        <NavLogo className="gradient-text-gold">NexusMarketing</NavLogo>
        <NavLinks>
          <NavLinkBase onClick={() => setActiveTab('home')} style={{ color: activeTab === 'home' ? 'var(--primary-neon)' : '' }}>Home</NavLinkBase>
          <NavLinkBase onClick={() => setActiveTab('abtest')} style={{ color: activeTab === 'abtest' ? 'var(--primary-neon)' : '' }}>A/B Simulator</NavLinkBase>
          <NavLinkBase onClick={() => setActiveTab('funnel')} style={{ color: activeTab === 'funnel' ? 'var(--primary-neon)' : '' }}>Funnel Strategy</NavLinkBase>
          <NavLinkBase onClick={() => setActiveTab('programmatic')} style={{ color: activeTab === 'programmatic' ? 'var(--primary-neon)' : '' }}>RTB Architecture</NavLinkBase>
          <NavLinkBase onClick={() => setActiveTab('mmm')} style={{ color: activeTab === 'mmm' ? 'var(--primary-neon)' : '' }}>Mix Modeling (MMM)</NavLinkBase>
        </NavLinks>
      </Navbar>

      <MainContent>
        <AnimatePresence mode="wait">
          {activeTab === 'home' && (
            <motion.div
              key="home"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Hero onNavigate={setActiveTab} />
            </motion.div>
          )}
          {activeTab === 'abtest' && (
            <motion.div
              key="abtest"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <ABTestingSimulator />
            </motion.div>
          )}
          {activeTab === 'funnel' && (
            <motion.div
              key="funnel"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <FunnelStrategy />
            </motion.div>
          )}
          {activeTab === 'programmatic' && (
            <motion.div
              key="programmatic"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <ProgrammaticAds />
            </motion.div>
          )}
          {activeTab === 'mmm' && (
            <motion.div
              key="mmm"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <DataScienceMMM />
            </motion.div>
          )}
        </AnimatePresence>
      </MainContent>

      <Footer>
        <p>&copy; {new Date().getFullYear()} Advanced Digital Marketing Portfolio. Built with React & Vite.</p>
      </Footer>
    </AppContainer>
  );
}

export default App;
