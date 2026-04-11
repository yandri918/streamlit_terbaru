import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Container = styled(motion.div)`
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
`;

const ControlsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 30px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const SliderCard = styled.div`
  background: rgba(20, 20, 30, 0.4);
  padding: 20px;
  border-radius: var(--border-radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);

  label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }

  input[type="range"] {
    width: 100%;
    accent-color: ${props => props.$color};
  }
`;

const MetricsContainer = styled.div`
  display: flex;
  gap: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
  justify-content: space-around;
  background: rgba(10, 10, 15, 0.6);
  padding: 20px;
  border-radius: var(--border-radius-sm);
`;

const MetricBox = styled.div`
  text-align: center;
  
  h4 {
    color: var(--text-secondary);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
  }
  
  p {
    font-family: var(--font-heading);
    font-size: 1.8rem;
    font-weight: 700;
    color: ${props => props.$color || 'var(--text-primary)'};
  }
`;

export default function MarketingDataScience() {
  const [tvSpend, setTvSpend] = useState(50);
  const [socialSpend, setSocialSpend] = useState(30);
  const [searchSpend, setSearchSpend] = useState(20);

  // Simulate a simplified linear regression MMM: Base Sales + (TV * effect) + (Social * effect) + (Search * effect)
  const baseSales = 200;
  const generateData = () => {
    const data = [];
    for(let week=1; week<=12; week++) {
      // Simulate weekly variations
      const tvEffect = (tvSpend * 1000) * 0.005 * (1 + (Math.sin(week) * 0.2));
      const socialEffect = (socialSpend * 1000) * 0.008 * (1 + (Math.cos(week) * 0.3));
      const searchEffect = (searchSpend * 1000) * 0.012 * (1 + (Math.sin(week*2) * 0.1));
      
      const totalSales = Math.floor(baseSales + tvEffect + socialEffect + searchEffect);
      
      data.push({
        week: `W${week}`,
        Sales: totalSales,
        TV_Contribution: Math.floor(tvEffect),
        Social_Contribution: Math.floor(socialEffect),
        Search_Contribution: Math.floor(searchEffect)
      });
    }
    return data;
  };

  const chartData = generateData();
  const totalSpend = tvSpend + socialSpend + searchSpend;
  const totalSales = chartData.reduce((acc, curr) => acc + curr.Sales, 0);
  const estimatedROAS = totalSpend > 0 ? (totalSales / (totalSpend * 1000 * 12)).toFixed(2) : 0; // Total sales / (Weekly spend * 12)

  return (
    <Container
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-panel"
      style={{ padding: '40px' }}
    >
      <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Marketing Mix Modeling (MMM)</h2>
      <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', maxWidth: '800px' }}>
        A statistical approach to attribute sales without user-level tracking (cookie-less). Adjust budget allocations across channels to see the simulated impact on incremental sales using linear regression models.
      </p>

      <ControlsGrid>
        <SliderCard $color="#8884d8">
          <label><span>TV Spend ($k/week)</span> <span style={{color: '#8884d8'}}>${tvSpend}k</span></label>
          <input type="range" min="0" max="100" value={tvSpend} onChange={(e) => setTvSpend(Number(e.target.value))} />
        </SliderCard>
        <SliderCard $color="#82ca9d">
          <label><span>Social Spend ($k/week)</span> <span style={{color: '#82ca9d'}}>${socialSpend}k</span></label>
          <input type="range" min="0" max="100" value={socialSpend} onChange={(e) => setSocialSpend(Number(e.target.value))} />
        </SliderCard>
        <SliderCard $color="var(--primary-neon)">
          <label><span>Search Spend ($k/week)</span> <span style={{color: 'var(--primary-neon)'}}>${searchSpend}k</span></label>
          <input type="range" min="0" max="100" value={searchSpend} onChange={(e) => setSearchSpend(Number(e.target.value))} />
        </SliderCard>
      </ControlsGrid>

      <MetricsContainer>
        <MetricBox $color="var(--text-primary)">
          <h4>Total Projected Sales</h4>
          <p>{totalSales.toLocaleString()}</p>
        </MetricBox>
        <MetricBox $color="var(--accent-gold)">
          <h4>Total Spend</h4>
          <p>${(totalSpend * 12).toLocaleString()}k</p>
        </MetricBox>
        <MetricBox $color={estimatedROAS > 1.5 ? '#00e676' : 'var(--secondary-neon)'}>
          <h4>Estimated ROAS</h4>
          <p>{estimatedROAS}x</p>
        </MetricBox>
      </MetricsContainer>

      <div style={{ height: '400px', marginTop: '30px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey="week" stroke="var(--text-secondary)" />
            <YAxis yAxisId="left" stroke="var(--text-secondary)" />
            <YAxis yAxisId="right" orientation="right" stroke="var(--primary-neon)" />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(10,10,15,0.95)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
              itemStyle={{ color: 'white' }}
            />
            <Legend />
            <Bar yAxisId="left" dataKey="TV_Contribution" stackId="a" fill="#8884d8" />
            <Bar yAxisId="left" dataKey="Social_Contribution" stackId="a" fill="#82ca9d" />
            <Bar yAxisId="left" dataKey="Search_Contribution" stackId="a" fill="var(--primary-neon)" />
            <Line yAxisId="right" type="monotone" dataKey="Sales" stroke="var(--accent-gold)" strokeWidth={3} dot={{r: 4}} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </Container>
  );
}
