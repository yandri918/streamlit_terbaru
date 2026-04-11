import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FaEye, FaMousePointer, FaShoppingCart, FaCreditCard, FaUserCheck } from 'react-icons/fa';

const FunnelContainer = styled(motion.div)`
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
`;

const FunnelStage = styled(motion.div)`
  display: flex;
  align-items: center;
  background: linear-gradient(90deg, rgba(20,20,30,0.8) 0%, rgba(30,30,45,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-sm);
  padding: 15px 25px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.2s ease;

  width: ${(props) => props.$width}%;
  margin: 0 auto;

  &:hover {
    transform: scale(1.02);
    border-color: var(--primary-neon);
    background: linear-gradient(90deg, rgba(30,30,45,0.9) 0%, rgba(40,40,60,0.6) 100%);
  }

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 4px;
    background: ${(props) => props.$color};
  }
`;

const StageIcon = styled.div`
  font-size: 1.5rem;
  color: ${(props) => props.$color};
  margin-right: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
`;

const StageInfo = styled.div`
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-primary);
  }

  span {
    font-size: 0.9rem;
    color: var(--text-secondary);
  }
`;

const StageMetrics = styled.div`
  text-align: right;
  
  .value {
    font-size: 1.2rem;
    font-weight: 700;
    font-family: var(--font-heading);
    color: var(--text-primary);
  }

  .dropoff {
    font-size: 0.8rem;
    color: var(--secondary-neon);
    margin-top: 4px;
  }
`;

const stageData = [
  { id: 'impressions', name: 'Impressions', icon: FaEye, color: '#00f0ff', initialValue: 100000, desc: 'Total ad views across networks' },
  { id: 'clicks', name: 'Clicks', icon: FaMousePointer, color: '#00c3ff', rate: 0.03, desc: 'Users who clicked the ad' }, // 3% CTR
  { id: 'add_to_cart', name: 'Add to Cart', icon: FaShoppingCart, color: '#4aa0ff', rate: 0.15, desc: 'Users who added items to cart' }, // 15% of clicks
  { id: 'checkout', name: 'Initiate Checkout', icon: FaCreditCard, color: '#887cff', rate: 0.40, desc: 'Users who started checkout' }, // 40% of ATC
  { id: 'purchase', name: 'Purchases', icon: FaUserCheck, color: '#c052ff', rate: 0.60, desc: 'Completed transactions' } // 60% of checkout
];

export default function FunnelStrategy() {
  const [baseTraffic, setBaseTraffic] = useState(100000);
  const [activeStage, setActiveStage] = useState(null);

  // Calculate funnel values based on rates
  const calculateFunnel = () => {
    let currentVal = baseTraffic;
    return stageData.map((stage, index) => {
      if (index === 0) return { ...stage, value: currentVal, dropoff: null };
      
      const previousVal = currentVal;
      currentVal = Math.floor(currentVal * stage.rate);
      const dropoffPercent = (((previousVal - currentVal) / previousVal) * 100).toFixed(1);

      return {
        ...stage,
        value: currentVal,
        dropoff: `-${dropoffPercent}% drop-off`
      };
    });
  };

  const currentFunnel = calculateFunnel();
  const maxVal = currentFunnel[0].value;

  return (
    <div style={{ width: '100%' }}>
      <div className="glass-panel" style={{ padding: '30px', marginBottom: '30px' }}>
         <h2 className="gradient-text" style={{ marginBottom: '10px' }}>Funnel Optimization Strategy</h2>
         <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
           Interactive visualization of a programmatic advertising conversion funnel. Adjust the top-of-funnel traffic to see downstream impacts.
         </p>
         
         <div style={{ marginBottom: '30px' }}>
            <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', marginBottom: '10px' }}>
              <span>Top-of-Funnel Traffic (Impressions)</span>
              <span style={{ color: 'white' }}>{baseTraffic.toLocaleString()}</span>
            </label>
            <input 
              type="range" 
              min="10000" 
              max="1000000" 
              step="10000" 
              value={baseTraffic} 
              onChange={(e) => setBaseTraffic(Number(e.target.value))} 
              style={{ width: '100%', accentColor: 'var(--primary-neon)' }}
            />
         </div>
      </div>

      <FunnelContainer>
        {currentFunnel.map((stage, index) => {
          const Icon = stage.icon;
          // Calculate width relative to max, but keep a minimum width so it doesn't disappear
          const widthPercent = Math.max((stage.value / maxVal) * 100, 30 + (5 - index)*10); // Artificial visual width adjustment for UI aesthetics

          return (
            <div key={stage.id} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
              <FunnelStage
                $width={widthPercent}
                $color={stage.color}
                onClick={() => setActiveStage(activeStage === stage.id ? null : stage.id)}
                layout
              >
                <StageIcon $color={stage.color}><Icon /></StageIcon>
                <StageInfo>
                  <div>
                    <h3>{stage.name}</h3>
                    <AnimatePresence>
                      {activeStage === stage.id && (
                        <motion.span
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          style={{ display: 'block', marginTop: '5px' }}
                        >
                          {stage.desc}
                        </motion.span>
                      )}
                    </AnimatePresence>
                  </div>
                </StageInfo>
                <StageMetrics>
                  <div className="value">{stage.value.toLocaleString()}</div>
                  {stage.dropoff && <div className="dropoff">{stage.dropoff}</div>}
                </StageMetrics>
              </FunnelStage>
              
              {/* Connector line between funnel stages */}
              {index < currentFunnel.length - 1 && (
                <div style={{ 
                  height: '20px', 
                  width: '2px', 
                  background: 'linear-gradient(to bottom, rgba(255,255,255,0.2), rgba(255,255,255,0.05))',
                  margin: '5px 0'
                }} />
              )}
            </div>
          );
        })}
      </FunnelContainer>
    </div>
  );
}
