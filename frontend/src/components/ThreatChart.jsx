import React from 'react';
import { motion } from 'framer-motion';

export const ThreatChart = ({ confidence, isMalicious }) => {
  const getColor = () => {
    if (confidence < 30) return 'hsl(var(--success))';
    if (confidence < 60) return 'hsl(40 100% 50%)';
    return 'hsl(var(--destructive))';
  };

  const categories = [
    { label: 'Signature Match', value: isMalicious ? Math.min(confidence + 5, 100) : 10 },
    { label: 'Behavior Analysis', value: isMalicious ? Math.min(confidence, 100) : 5 },
    { label: 'Entropy Score', value: isMalicious ? Math.min(confidence - 10, 100) : 8 },
    { label: 'String Detection', value: isMalicious ? Math.min(confidence + 10, 100) : 12 },
  ];

  return (
    <div className="space-y-4">
      {categories.map((category, index) => (
        <div key={category.label}>
          <div className="flex justify-between mb-2 text-sm">
            <span className="text-muted-foreground">{category.label}</span>
            <span className="font-mono text-foreground">{category.value}%</span>
          </div>
          <div className="h-3 bg-secondary rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${category.value}%` }}
              transition={{ delay: index * 0.1, duration: 0.8, ease: 'easeOut' }}
              className="h-full rounded-full"
              style={{
                background: `linear-gradient(90deg, ${getColor()}, ${getColor()}cc)`,
                boxShadow: `0 0 10px ${getColor()}`,
              }}
            />
          </div>
        </div>
      ))}
      
      <div className="mt-6 pt-4 border-t border-border">
        <div className="flex justify-between items-center">
          <span className="text-sm font-semibold text-foreground">Overall Confidence</span>
          <span className="text-2xl font-bold font-mono" style={{ color: getColor() }}>
            {confidence}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default ThreatChart;