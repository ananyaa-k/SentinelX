import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, RefreshCw, AlertTriangle, Shield, Bug, FileWarning, Download, Filter } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Checkbox } from "../components/ui/checkbox"
import { Label } from "../components/ui/label"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuCheckboxItem,
  DropdownMenuTrigger,
} from "../components/ui/dropdown-menu"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';
import { toast } from 'sonner';
import axios from 'axios';

export const ThreatIntelPage = () => {
  const [rules, setRules] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [syncing, setSyncing] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // Sync Sources State
  const [syncSources, setSyncSources] = useState({
    github: true,
    otx: true,
    malwarebazaar: true
  });

  const fetchRules = async () => {
    setLoading(true);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const response = await axios.get(`${backendUrl}/api/rules`);
      setRules(response.data);
    } catch (error) {
      console.error("Failed to fetch rules", error);
      toast.error("Failed to load rules.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleSync = async () => {
    const activeSources = Object.keys(syncSources).filter(k => syncSources[k]);
    
    if (activeSources.length === 0) {
      toast.error("Please select at least one source to sync.");
      return;
    }

    setSyncing(true);
    toast.info(`Syncing from: ${activeSources.join(', ')}...`);
    
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      await axios.post(`${backendUrl}/api/sync-rules`, { sources: activeSources });
      
      toast.success('Sync started in background.');
      
      setTimeout(() => {
        fetchRules();
      }, 5000);

    } catch (error) {
      toast.error('Sync trigger failed.');
    } finally {
      setSyncing(false);
    }
  };

  const handleDownload = (rule) => {
    const element = document.createElement("a");
    const file = new Blob([rule.content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `${rule.name}.yar`;
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
    document.body.removeChild(element);
    toast.success(`Downloaded ${rule.name}.yar`);
  };

  const filteredRules = rules.filter(rule =>
    rule.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (rule.family && rule.family.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (rule.rule_id && rule.rule_id.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'destructive';
      case 'high':
        return 'default';
      case 'medium':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  return (
    <div className="min-h-screen p-8 bg-background transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 className="text-4xl font-display font-bold text-primary mb-2">Threat Intelligence</h1>
            <p className="text-muted-foreground">Manage and synchronize global YARA signatures</p>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <Card className="bg-card border-border">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Total Rules</p>
                  <p className="text-2xl font-bold text-foreground">{rules.length}</p>
                </div>
                <Shield className="w-8 h-8 text-primary" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-card border-border">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Critical</p>
                  <p className="text-2xl font-bold text-destructive">
                    {rules.filter(r => r.severity?.toLowerCase() === 'critical').length}
                  </p>
                </div>
                <AlertTriangle className="w-8 h-8 text-destructive" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-card border-border">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">High Priority</p>
                  <p className="text-2xl font-bold text-foreground">
                    {rules.filter(r => r.severity?.toLowerCase() === 'high').length}
                  </p>
                </div>
                <FileWarning className="w-8 h-8 text-primary" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-card border-border">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Sources</p>
                  <p className="text-2xl font-bold text-foreground">
                     {new Set(rules.map(r => r.source)).size}
                  </p>
                </div>
                <Bug className="w-8 h-8 text-success" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Actions Bar */}
        <Card className="bg-card border-border mb-6">
          <CardHeader className="py-4">
            <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
              
              {/* Search */}
              <div className="relative w-full lg:w-96">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search rules..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 bg-secondary border-border"
                />
              </div>

              {/* Sync Controls */}
              <div className="flex items-center gap-3 w-full lg:w-auto">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" className="gap-2">
                      <Filter className="w-4 h-4" />
                      Sync Sources
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-56">
                    <DropdownMenuLabel>Select Feeds</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuCheckboxItem
                      checked={syncSources.github}
                      onCheckedChange={(c) => setSyncSources(prev => ({...prev, github: c}))}
                    >
                      ReversingLabs (GitHub)
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem
                      checked={syncSources.otx}
                      onCheckedChange={(c) => setSyncSources(prev => ({...prev, otx: c}))}
                    >
                      AlienVault OTX
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem
                      checked={syncSources.malwarebazaar}
                      onCheckedChange={(c) => setSyncSources(prev => ({...prev, malwarebazaar: c}))}
                    >
                      MalwareBazaar
                    </DropdownMenuCheckboxItem>
                  </DropdownMenuContent>
                </DropdownMenu>

                <Button
                  onClick={handleSync}
                  disabled={syncing}
                  className="bg-primary text-primary-foreground hover:bg-primary/90 glow-cyan min-w-[140px]"
                >
                  {syncing ? (
                    <>
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                      Syncing...
                    </>
                  ) : (
                    <>
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Sync Now
                    </>
                  )}
                </Button>
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* Rules Table */}
        <Card className="bg-card border-border shadow-md">
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-border hover:bg-transparent">
                    <TableHead className="w-[100px]">Download</TableHead>
                    <TableHead>Rule Name</TableHead>
                    <TableHead>Family</TableHead>
                    <TableHead>Severity</TableHead>
                    <TableHead>Source</TableHead>
                    <TableHead className="text-right">Date</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredRules.map((rule, index) => (
                    <motion.tr
                      key={rule.id || index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-border hover:bg-secondary/50 transition-colors group"
                    >
                      <TableCell>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-8 w-8 text-muted-foreground hover:text-primary"
                          onClick={() => handleDownload(rule)}
                          title="Download .yar file"
                        >
                          <Download className="w-4 h-4" />
                        </Button>
                      </TableCell>
                      <TableCell className="font-semibold text-foreground">{rule.name}</TableCell>
                      <TableCell>{rule.family}</TableCell>
                      <TableCell>
                        <Badge variant={getSeverityColor(rule.severity)}>
                          {rule.severity}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="text-xs">
                          {rule.source}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right text-muted-foreground font-mono text-xs">
                        {rule.date_added ? new Date(rule.date_added).toLocaleDateString() : 'N/A'}
                      </TableCell>
                    </motion.tr>
                  ))}
                </TableBody>
              </Table>
            </div>
            
            {!loading && filteredRules.length === 0 && (
              <div className="text-center py-12">
                <Search className="w-12 h-12 mx-auto mb-4 text-muted-foreground/50" />
                <p className="text-muted-foreground">No rules found matching your search</p>
              </div>
            )}
             {loading && (
               <div className="text-center py-12">
                 <RefreshCw className="w-8 h-8 mx-auto mb-4 text-primary animate-spin" />
                 <p className="text-muted-foreground">Loading rules database...</p>
               </div>
             )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ThreatIntelPage;
