import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Zap, Search, Eye, Server, Lock, Code, Cpu, Layers } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Link } from 'react-router-dom';

const BriefingPage = () => {
  return (
    <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-32">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="flex flex-col items-center text-center space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-primary text-primary-foreground hover:bg-primary/80 mb-6">
                v2.0 Enterprise Edition
              </div>
              <h1 className="text-4xl font-extrabold tracking-tight lg:text-6xl mb-4">
                SentinelX <span className="text-primary">Defender</span>
              </h1>
              <p className="max-w-[700px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed mx-auto">
                Advanced malware analysis platform powered by YARA signatures and Gemini AI.
                Protect your infrastructure with autonomous threat detection and real-time intelligence feeds.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4"
            >
              <Button asChild size="lg" className="h-12 px-8">
                <Link to="/command-center">Launch Scanner</Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="h-12 px-8">
                <Link to="/threat-intel">View Threat Feed</Link>
              </Button>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-24 bg-secondary/30">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="pt-6">
                <Shield className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-bold mb-2">Hybrid Detection Engine</h3>
                <p className="text-muted-foreground">
                  Combines high-speed static analysis using YARA rules with heuristic AI analysis powered by Gemini 2.5 Flash.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="pt-6">
                <Zap className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-bold mb-2">Autonomous Rule Gen</h3>
                <p className="text-muted-foreground">
                  Automatically generates and compiles new YARA signatures for zero-day threats detected by our AI engine.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border hover:border-primary/50 transition-colors">
              <CardContent className="pt-6">
                <Server className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-bold mb-2">Global Intelligence</h3>
                <p className="text-muted-foreground">
                  Real-time synchronization with MalwareBazaar, OTX, and ReversingLabs repositories for up-to-the-minute protection.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Deep Dive Sections */}
      <section className="py-24">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 text-primary font-semibold">
                <Code className="w-5 h-5" />
                <span>The Technology</span>
              </div>
              <h2 className="text-3xl font-bold">Powered by YARA</h2>
              <p className="text-muted-foreground leading-relaxed">
                YARA (Yet Another Recursive Acronym) is the industry standard for identifying and classifying malware samples.
                It allows us to create descriptions of malware families based on textual or binary patterns.
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  <span>Pattern-based identification of malware families</span>
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  <span>Lightweight and extremely fast scanning</span>
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  <span>Industry-standard rule syntax</span>
                </li>
              </ul>
            </div>
            <div className="bg-card border rounded-xl p-8 shadow-xl font-mono text-sm relative overflow-hidden group">
              <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity" />
              <p className="text-muted-foreground mb-4"># Example YARA Rule Structure</p>
              <pre className="text-foreground">
                {`rule Silent_Banker_Trojan {
    meta:
        description = "Detects banking trojan variant"
        severity = "Critical"
    strings:
        $s1 = "cmd.exe /c start" 
        $s2 = "CreateRemoteThread"
        $hex = { 4D 5A 90 00 03 00 }
    condition:
        $hex at 0 and ($s1 or $s2)
}`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-24 bg-primary/5">
        <div className="container px-4 md:px-6 mx-auto text-center">
          <h2 className="text-3xl font-bold mb-12">Why Enterprises Choose SentinelX</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-2xl bg-background border flex items-center justify-center mb-4 shadow-sm">
                <Cpu className="w-8 h-8 text-primary" />
              </div>
              <h4 className="font-semibold mb-2">AI-Driven</h4>
              <p className="text-sm text-muted-foreground">Gemini 2.5 Analysis</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-2xl bg-background border flex items-center justify-center mb-4 shadow-sm">
                <Layers className="w-8 h-8 text-primary" />
              </div>
              <h4 className="font-semibold mb-2">Multi-Layered</h4>
              <p className="text-sm text-muted-foreground">Static + Heuristic</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-2xl bg-background border flex items-center justify-center mb-4 shadow-sm">
                <Lock className="w-8 h-8 text-primary" />
              </div>
              <h4 className="font-semibold mb-2">Private</h4>
              <p className="text-sm text-muted-foreground">Secure Processing</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-2xl bg-background border flex items-center justify-center mb-4 shadow-sm">
                <Eye className="w-8 h-8 text-primary" />
              </div>
              <h4 className="font-semibold mb-2">Transparent</h4>
              <p className="text-sm text-muted-foreground">Explainable AI</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default BriefingPage;
