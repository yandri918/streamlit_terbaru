import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const HeroSection = styled.section`
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
  padding: 20px;
`;

const Badge = styled(motion.div)`
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid rgba(0, 240, 255, 0.3);
  color: var(--primary-neon);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 30px;
  display: inline-block;
`;

const Title = styled(motion.h1)`
  font-size: clamp(2.5rem, 8vw, 5.5rem);
  line-height: 1.1;
  margin-bottom: 24px;
  max-width: 1000px;
  
  span {
    display: block;
  }
`;

const Description = styled(motion.p)`
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: var(--text-secondary);
  max-width: 700px;
  margin-bottom: 40px;
  line-height: 1.6;
`;

const ButtonGroup = styled(motion.div)`
  display: flex;
  gap: 20px;
  
  @media (max-width: 600px) {
    flex-direction: column;
    width: 100%;
    max-width: 300px;
  }
`;

const PrimaryButton = styled.button`
  background: var(--primary-neon);
  color: var(--bg-dark);
  border: none;
  padding: 16px 32px;
  border-radius: var(--border-radius-sm);
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 15px var(--primary-glow);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px var(--primary-glow);
    background: #00ffff;
  }
`;

const SecondaryButton = styled.button`
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 16px 32px;
  border-radius: var(--border-radius-sm);
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
  }
`;

export default function Hero({ onNavigate }) {
  return (
    <HeroSection>
      <Badge
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        Advanced Growth Engineering
      </Badge>
      
      <Title
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <span>Data-Driven</span>
        <span className="gradient-text">Marketing Architecture</span>
      </Title>
      
      <Description
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.4 }}
      >
        Shift from intuition to precision. Master algorithmic funnel optimization, statistical A/B testing, and ROAS maximization strategies.
      </Description>
      
      <ButtonGroup
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <PrimaryButton onClick={() => onNavigate('abtest')}>
          Launch Simulator
        </PrimaryButton>
        <SecondaryButton onClick={() => onNavigate('funnel')}>
          View Funnel Strategy
        </SecondaryButton>
      </ButtonGroup>
    </HeroSection>
  );
}
