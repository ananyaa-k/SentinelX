import React from 'react';
import { motion } from 'framer-motion';
import { FileText, ArrowRight, ShieldCheck, ShieldAlert, Brain, Database, Code, Cog } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

const AiLogicPage = () => {
  return (
    <div className="min-h-screen p-8 bg-background">
      <div className="max-w-7xl mx-auto">
        <div className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-primary mb-4">Autonomous Detection Pipeline</h1>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Visualizing the decision flow from file ingestion to signature generation.
          </p>
        </div>

        {/* Pipeline Visualization */}
        <div className="relative">
          {/* Connector Line (Desktop) */}
          <div className="hidden lg:block absolute top-1/2 left-0 w-full h-1 bg-gradient-to-r from-primary/20 via-primary/50 to-primary/20 -translate-y-1/2 z-0" />

          <div className="grid lg:grid-cols-5 gap-8 relative z-10">
            {/* Step 1: Ingestion */}
            <PipelineStep 
              icon={FileText} 
              title="1. Ingestion" 
              desc="File upload & Pre-processing" 
              color="text-foreground"
            />

            {/* Step 2: Static Analysis */}
            <PipelineStep 
              icon={Code} 
              title="2. YARA Scan" 
              desc="Match against existing signature DB" 
              color="text-blue-500"
            />

            {/* Branching Logic (Visual Only) */}
            <div className="lg:col-span-1 flex flex-col items-center justify-center space-y-4">
              <div className="bg-card border p-4 rounded-lg shadow-lg text-center w-full">
                <p className="font-bold text-sm mb-2">Match Found?</p>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-green-500 font-bold">YES</span>
                  <span className="text-red-500 font-bold">NO</span>
                </div>
              </div>
            </div>

            {/* Step 3: AI Analysis */}
            <PipelineStep 
              icon={Brain} 
              title="3. Gemini AI" 
              desc="Deep heuristic analysis of unknown files" 
              color="text-purple-500"
            />

            {/* Step 4: Rule Gen */}
            <PipelineStep 
              icon={Database} 
              title="4. Synthesis" 
              desc="Auto-generate & compile new YARA rule" 
              color="text-orange-500"
            />
          </div>
        </div>

        {/* Detailed Logic Flows */}
        <div className="mt-24 grid md:grid-cols-2 gap-12">
          
          {/* Path A: Fast Match */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            className="space-y-4"
          >
            <div className="flex items-center gap-3 mb-6">
              <ShieldCheck className="w-8 h-8 text-green-500" />
              <h2 className="text-2xl font-bold">Path A: Known Threat</h2>
            </div>
            <Card className="bg-card border-l-4 border-l-green-500">
              <CardContent className="pt-6">
                <ol className="space-y-4 relative border-l border-muted ml-3 pl-6">
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-green-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">YARA Engine Scan</p>
                    <p className="text-sm text-muted-foreground">Scans file against 50,000+ local rules.</p>
                  </li>
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-green-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">Signature Match</p>
                    <p className="text-sm text-muted-foreground">Immediate identification (e.g., "Win32.Emotet").</p>
                  </li>
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-green-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">Block & Report</p>
                    <p className="text-sm text-muted-foreground">Zero-latency verdict. No AI cost incurred.</p>
                  </li>
                </ol>
              </CardContent>
            </Card>
          </motion.div>

          {/* Path B: Zero-Day */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            className="space-y-4"
          >
            <div className="flex items-center gap-3 mb-6">
              <ShieldAlert className="w-8 h-8 text-orange-500" />
              <h2 className="text-2xl font-bold">Path B: Zero-Day Discovery</h2>
            </div>
            <Card className="bg-card border-l-4 border-l-orange-500">
              <CardContent className="pt-6">
                <ol className="space-y-4 relative border-l border-muted ml-3 pl-6">
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-orange-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">AI Heuristics (Gemini 2.5)</p>
                    <p className="text-sm text-muted-foreground">Analyzes entropy, strings, and code structure.</p>
                  </li>
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-orange-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">Threat Confirmation</p>
                    <p className="text-sm text-muted-foreground">AI identifies malicious intent (e.g., "Reverse Shell").</p>
                  </li>
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-orange-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">Rule Generation</p>
                    <p className="text-sm text-muted-foreground">System auto-writes a new YARA signature.</p>
                  </li>
                  <li className="relative">
                    <span className="absolute -left-[31px] bg-orange-500 w-2.5 h-2.5 rounded-full mt-1.5" />
                    <p className="font-semibold">Database Update</p>
                    <p className="text-sm text-muted-foreground">New rule is deployed instantly to local DB.</p>
                  </li>
                </ol>
              </CardContent>
            </Card>
          </motion.div>

        </div>
      </div>
    </div>
  );
};

const PipelineStep = ({ icon: Icon, title, desc, color }) => (
  <motion.div 
    whileHover={{ y: -5 }}
    className="bg-card border rounded-xl p-6 shadow-sm relative z-10 flex flex-col items-center text-center"
  >
    <div className={`p-4 rounded-full bg-secondary mb-4 ${color}`}>
      <Icon className="w-8 h-8" />
    </div>
    <h3 className="font-bold text-lg mb-2">{title}</h3>
    <p className="text-sm text-muted-foreground">{desc}</p>
  </motion.div>
);

export default AiLogicPage;
