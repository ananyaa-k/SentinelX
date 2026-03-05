import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Shield, AlertTriangle, CheckCircle2, Loader2, Brain, FileText, Hash, ThumbsUp, ThumbsDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { Alert, AlertDescription, AlertTitle } from '../components/ui/alert';
import ThreatChart from '../components/ThreatChart';
import axios from 'axios';
import { toast } from 'sonner';

export const CommandCenterPage = () => {
  const [file, setFile] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [scanStage, setScanStage] = useState('');
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile) => {
    setFile(selectedFile);
    setResult(null);
    performScan(selectedFile);
  };

  const performScan = async (selectedFile) => {
    setScanning(true);
    setProgress(0);
    setResult(null);

    setScanStage('Uploading...');
    setProgress(10);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const backendUrl = process.env.REACT_APP_BACKEND_URL;

      const response = await fetch(`${backendUrl}/api/scan`, {
        method: 'POST',
        headers: {},
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status} ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      let finalData = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.substring(6).trim();
            if (!dataStr) continue;

            try {
              const data = JSON.parse(dataStr);
              if (data.error) {
                throw new Error(data.error);
              }
              if (data.stage) setScanStage(data.stage);
              if (data.progress) setProgress(data.progress);
              if (data.result) {
                finalData = data.result;
              }
            } catch (e) {
              if (e.message !== 'Unexpected end of JSON input') {
                console.error('JSON parse error:', e, dataStr);
              }
            }
          }
        }
      }

      if (finalData) {
        setResult({
          scanId: finalData.id,
          status: finalData.status,
          confidence: finalData.confidence,
          detectedStrings: finalData.detected_rules || [],
          fileName: finalData.filename,
          fileSize: finalData.filesize,
          fileType: finalData.filetype,
          analysisTime: Date.now(),
          aiInsight: finalData.ai_insight,
        });

        if (finalData.status === 'MALICIOUS') {
          toast.error(`Threat Detected: ${finalData.filename}`);
        } else {
          toast.success(`Scan Complete: File appears safe.`);
        }
      } else {
        throw new Error("No result returned from stream.");
      }

    } catch (error) {
      console.error("Scan failed", error);
      toast.error("Scan failed: " + error.message);
      setResult(null);
    } finally {
      setScanning(false);
      setScanStage('');
    }
  };

  const submitFeedback = async (decision) => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      await axios.post(`${backendUrl}/api/scan/feedback`, {
        scan_id: result.scanId || 'unknown',
        filename: result.fileName,
        analyst_decision: decision,
        notes: ''
      });
      toast.success('Feedback recorded. Gemini agent will learn from this in future scans.');
    } catch (error) {
      console.error(error);
      toast.error('Failed to submit feedback.');
    }
  };

  return (
    <div className="min-h-screen p-8 bg-background transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold text-primary mb-2">Command Center</h1>
          <p className="text-muted-foreground">Upload files for deep-inspection analysis</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <div className="space-y-6">
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5 text-primary" />
                  File Upload Zone
                </CardTitle>
                <CardDescription>Drag and drop or click to upload suspicious files</CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-all duration-300 ${dragActive
                      ? 'border-primary bg-primary/10 glow-cyan'
                      : 'border-border hover:border-primary/50'
                    }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    onChange={handleFileInput}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    accept="*/*"
                  />

                  <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-foreground font-semibold mb-2">Drop files here</p>
                  <p className="text-sm text-muted-foreground">or click to browse</p>
                </div>

                {file && !scanning && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 p-4 bg-secondary rounded-lg"
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="w-5 h-5 text-primary" />
                      <div className="flex-1 min-w-0">
                        <p className="font-mono text-sm truncate">{file.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {(file.size / 1024).toFixed(2)} KB
                        </p>
                      </div>
                    </div>
                  </motion.div>
                )}
              </CardContent>
            </Card>

            <AnimatePresence>
              {scanning && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <Card className="bg-card border-primary">
                    <CardContent className="pt-6">
                      <div className="space-y-4">
                        <div className="flex items-center gap-3">
                          <Loader2 className="w-5 h-5 text-primary animate-spin" />
                          <span className="text-sm font-mono text-primary">{scanStage}</span>
                        </div>
                        <Progress value={progress} className="h-2" />
                        <p className="text-xs text-muted-foreground text-center">
                          Running static analysis and AI heuristics...
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="space-y-6">
            <AnimatePresence>
              {result && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="space-y-6"
                >
                  <Alert
                    variant={result.status === 'MALICIOUS' ? 'destructive' : 'default'}
                    className={result.status === 'MALICIOUS' ? 'border-destructive glow-red' : 'border-success glow-green'}
                  >
                    {result.status === 'MALICIOUS' ? (
                      <AlertTriangle className="h-5 w-5" />
                    ) : (
                      <CheckCircle2 className="h-5 w-5" />
                    )}
                    <AlertTitle className="text-lg font-display">
                      Status: {result.status}
                    </AlertTitle>
                    <AlertDescription>
                      Threat confidence: {result.confidence}%
                    </AlertDescription>
                  </Alert>

                  <Card className="bg-card border-border">
                    <CardHeader>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <Hash className="w-4 h-4" />
                        File Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="grid grid-cols-2 gap-3 text-sm">
                        <div>
                          <p className="text-muted-foreground">Filename</p>
                          <p className="font-mono truncate">{result.fileName}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Size</p>
                          <p className="font-mono">{(result.fileSize / 1024).toFixed(2)} KB</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Type</p>
                          <p className="font-mono">{result.fileType}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Confidence</p>
                          <p className="font-mono">{result.confidence}%</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {result.detectedStrings.length > 0 && (
                    <Card className="bg-card border-destructive/50">
                      <CardHeader>
                        <CardTitle className="text-lg flex items-center gap-2 text-destructive">
                          <AlertTriangle className="w-4 h-4" />
                          Detected Threats / YARA Rules
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="flex flex-wrap gap-2">
                          {result.detectedStrings.map((str, index) => (
                            <Badge key={index} variant="destructive" className="font-mono">
                              {str}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  )}

                  <Card className="bg-card border-accent/50">
                    <CardHeader>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <Brain className="w-4 h-4 text-accent" />
                        Gemini Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                        {result.aiInsight}
                      </p>
                    </CardContent>
                  </Card>

                  <Card className="bg-card border-border">
                    <CardHeader>
                      <CardTitle className="text-lg">Threat Confidence Score</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ThreatChart confidence={result.confidence} isMalicious={result.status === 'MALICIOUS'} />
                    </CardContent>
                  </Card>

                  <div className="flex flex-col sm:flex-row justify-end gap-3 mt-4 pt-4 border-t border-border">
                    <span className="text-sm text-muted-foreground mr-auto self-center">Help the AI agent learn by providing feedback.</span>
                    <Button variant="outline" size="sm" onClick={() => submitFeedback('FALSE_POSITIVE')}>
                      <ThumbsDown className="w-4 h-4 mr-2" />
                      Mark False Positive
                    </Button>
                    <Button variant="default" size="sm" onClick={() => submitFeedback('TRUE_POSITIVE')}>
                      <ThumbsUp className="w-4 h-4 mr-2" />
                      Confirm Threat
                    </Button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {!result && !scanning && (
              <Card className="bg-card border-border">
                <CardContent className="pt-6">
                  <div className="text-center py-12">
                    <Shield className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
                    <p className="text-muted-foreground">Upload a file to begin analysis</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CommandCenterPage;
