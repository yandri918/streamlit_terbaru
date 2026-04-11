import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

const Container = styled(motion.div)`
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
`;

const ArchitectureDiagram = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 40px;
  position: relative;
  flex-wrap: wrap;
  gap: 20px;

  @media (max-width: 900px) {
    flex-direction: column;
  }
`;

const Node = styled(motion.div)`
  background: ${props => props.$active ? 'rgba(0, 240, 255, 0.15)' : 'rgba(20, 20, 30, 0.6)'};
  border: 1px solid ${props => props.$active ? 'var(--primary-neon)' : 'rgba(255, 255, 255, 0.1)'};
  border-radius: var(--border-radius-sm);
  padding: 20px;
  width: 200px;
  text-align: center;
  cursor: pointer;
  z-index: 2;
  box-shadow: ${props => props.$active ? '0 0 20px var(--primary-glow)' : 'none'};
  transition: all 0.3s ease;

  h3 {
    color: ${props => props.$active ? 'var(--primary-neon)' : 'var(--text-primary)'};
    margin-bottom: 8px;
    font-size: 1.2rem;
  }

  p {
    font-size: 0.85rem;
    color: var(--text-secondary);
  }

  &:hover {
    transform: translateY(-5px);
    border-color: rgba(0, 240, 255, 0.5);
  }
`;

const FlowLine = styled.div`
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, 
    rgba(255,255,255,0.1) 0%, 
    ${props => props.$active ? 'var(--primary-neon)' : 'rgba(255,255,255,0.2)'} 50%, 
    rgba(255,255,255,0.1) 100%);
  position: relative;
  min-width: 50px;
  
  @media (max-width: 900px) {
    width: 2px;
    height: 40px;
    background: linear-gradient(180deg, rgba(255,255,255,0.1), ${props => props.$active ? 'var(--primary-neon)' : 'rgba(255,255,255,0.2)'}, rgba(255,255,255,0.1));
  }
`;

const DetailPanel = styled(motion.div)`
  margin-top: 40px;
  padding: 30px;
  background: rgba(10, 10, 15, 0.8);
  border: 1px solid var(--primary-neon);
  border-radius: var(--border-radius);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
`;

const nodesData = [
  {
    id: 'advertiser',
    title: 'Advertiser / Agency',
    desc: 'Sets campaign goals, budget, and tracking.',
    detail: "The brand that wants to buy ad space to reach their target audience. They define the targeting criteria (demographics, intent, retargeting) and set the maximum bid they are willing to pay for an impression."
  },
  {
    id: 'dsp',
    title: 'DSP (Demand-Side)',
    desc: 'Automates buying of ad inventory.',
    detail: "Demand-Side Platform: Software used by advertisers to purchase display, video, mobile, and search ads in an automated fashion. It plugs into multiple Ad Exchanges and evaluates inventory on a per-impression basis, placing bids in microseconds using algorithms."
  },
  {
    id: 'exchange',
    title: 'Ad Exchange (RTB)',
    desc: 'The real-time auction marketplace.',
    detail: "The digital marketplace where the actual transaction occurs. When a user loads a webpage, the exchange receives the bid request from the SSP, holds a Real-Time Bidding (RTB) auction in under 100ms, and awards the impression to the highest bidding DSP."
  },
  {
    id: 'ssp',
    title: 'SSP (Supply-Side)',
    desc: 'Maximizes yield for publishers.',
    detail: "Supply-Side Platform: Software used by publishers to automate the sale of their advertising space. It connects to ad exchanges and DSPs to ensure the publisher gets the highest possible price for their inventory."
  },
  {
    id: 'publisher',
    title: 'Publisher',
    desc: 'Website or app hosting the ad.',
    detail: "The owner of the website or app that the user is visiting. They provide the 'inventory' (ad slots) and generate revenue when impressions are sold to advertisers via the SSP."
  }
];

export default function ProgrammaticAds() {
  const [activeNode, setActiveNode] = useState(nodesData[2]); // Default to Exchange

  return (
    <Container
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-panel"
      style={{ padding: '40px' }}
    >
      <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '15px' }}>Programmatic Ad Architecture</h2>
      <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', maxWidth: '800px', marginBottom: '30px' }}>
        Interactive breakdown of the Real-Time Bidding (RTB) ecosystem. Click on a component to understand its technical role in the 100-millisecond auction lifecycle.
      </p>

      <ArchitectureDiagram>
        {nodesData.map((node, index) => (
          <React.Fragment key={node.id}>
            <Node 
              $active={activeNode.id === node.id}
              onClick={() => setActiveNode(node)}
              whileTap={{ scale: 0.95 }}
            >
              <h3>{node.title}</h3>
              <p>{node.desc}</p>
            </Node>
            {index < nodesData.length - 1 && (
              <FlowLine $active={activeNode.id === node.id || activeNode.id === nodesData[index + 1].id} />
            )}
          </React.Fragment>
        ))}
      </ArchitectureDiagram>

      <AnimatePresence mode="wait">
        <DetailPanel
          key={activeNode.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          <h3 style={{ color: 'var(--primary-neon)', fontSize: '1.5rem', marginBottom: '15px' }}>{activeNode.title} Deep Dive</h3>
          <p style={{ color: 'var(--text-primary)', fontSize: '1.1rem', lineHeight: '1.7' }}>
            {activeNode.detail}
          </p>
        </DetailPanel>
      </AnimatePresence>

    </Container>
  );
}
