import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const SimulatorContainer = styled(motion.div)`
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
`;

const ControlsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
`;

const ControlGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  background: rgba(20, 20, 30, 0.4);
  border-radius: var(--border-radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);

  label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    display: flex;
    justify-content: space-between;
  }

  input[type="range"] {
    width: 100%;
    accent-color: var(--primary-neon);
  }
`;

const ChartContainer = styled.div`
  height: 400px;
  width: 100%;
  padding: 20px;
  background: rgba(10, 10, 15, 0.6);
  border-radius: var(--border-radius);
  border: 1px solid rgba(255, 255, 255, 0.05);
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const MetricCard = styled.div`
  padding: 20px;
  background: linear-gradient(145deg, rgba(30,30,40,0.8) 0%, rgba(20,20,30,0.8) 100%);
  border-radius: var(--border-radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);
  text-align: center;

  h4 {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  p {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: var(--font-heading);
  }
`;

export default function ABTestingSimulator() {
  const [traffic, setTraffic] = useState(10000);
  const [crA, setCrA] = useState(2.5); // Control Conversion Rate %
  const [crB, setCrB] = useState(3.2); // Variant Conversion Rate %
  const [data, setData] = useState([]);

  useEffect(() => {
    // Generate simulation data over 14 days
    const newData = [];
    let cumulativeA = 0;
    let cumulativeB = 0;
    const dailyTraffic = Math.floor(traffic / 14);

    for (let day = 1; day <= 14; day++) {
      // Add some randomness to daily conversions
      const dailyConvA = Math.floor(dailyTraffic * (crA / 100) * (0.8 + Math.random() * 0.4));
      const dailyConvB = Math.floor(dailyTraffic * (crB / 100) * (0.8 + Math.random() * 0.4));
      
      cumulativeA += dailyConvA;
      cumulativeB += dailyConvB;

      newData.push({
        day: `Day ${day}`,
        Control: cumulativeA,
        Variant: cumulativeB,
      });
    }
    setData(newData);
  }, [traffic, crA, crB]);

  const totalConversionsA = data.length > 0 ? data[data.length - 1].Control : 0;
  const totalConversionsB = data.length > 0 ? data[data.length - 1].Variant : 0;
  const uplift = totalConversionsA > 0 ? (((totalConversionsB - totalConversionsA) / totalConversionsA) * 100).toFixed(2) : 0;

  return (
    <SimulatorContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-panel"
      style={{ padding: '30px' }}
    >
      <h2 className="gradient-text" style={{ marginBottom: '10px' }}>A/B Testing Simulator</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
        Visualize the impact of Conversion Rate Optimization (CRO) over a 14-day test period.
      </p>

      <ControlsGrid>
        <ControlGroup>
          <label><span>Total Traffic (14 Days)</span> <span style={{ color: 'white' }}>{traffic.toLocaleString()}</span></label>
          <input 
            type="range" 
            min="1000" 
            max="100000" 
            step="1000" 
            value={traffic} 
            onChange={(e) => setTraffic(Number(e.target.value))} 
          />
        </ControlGroup>
        <ControlGroup>
          <label><span>Control CR (Version A)</span> <span style={{ color: 'white' }}>{crA.toFixed(1)}%</span></label>
          <input 
            type="range" 
            min="0.5" 
            max="10" 
            step="0.1" 
            value={crA} 
            onChange={(e) => setCrA(Number(e.target.value))} 
          />
        </ControlGroup>
        <ControlGroup>
          <label><span>Variant CR (Version B)</span> <span style={{ color: 'white' }}>{crB.toFixed(1)}%</span></label>
          <input 
            type="range" 
            min="0.5" 
            max="10" 
            step="0.1" 
            value={crB} 
            onChange={(e) => setCrB(Number(e.target.value))} 
          />
        </ControlGroup>
      </ControlsGrid>

      <MetricsGrid>
        <MetricCard>
          <h4>Control Conversions</h4>
          <p style={{ color: '#8884d8' }}>{totalConversionsA.toLocaleString()}</p>
        </MetricCard>
        <MetricCard>
          <h4>Variant Conversions</h4>
          <p style={{ color: 'var(--primary-neon)' }}>{totalConversionsB.toLocaleString()}</p>
        </MetricCard>
        <MetricCard>
          <h4>Relative Uplift</h4>
          <p style={{ color: uplift > 0 ? '#00e676' : 'var(--secondary-neon)' }}>
            {uplift > 0 ? '+' : ''}{uplift}%
          </p>
        </MetricCard>
      </MetricsGrid>

      <ChartContainer>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="day" stroke="var(--text-secondary)" />
            <YAxis stroke="var(--text-secondary)" />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(10,10,15,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
              itemStyle={{ color: 'white' }}
            />
            <Legend />
            <Line type="monotone" dataKey="Control" stroke="#8884d8" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
            <Line type="monotone" dataKey="Variant" stroke="var(--primary-neon)" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    </SimulatorContainer>
  );
}
