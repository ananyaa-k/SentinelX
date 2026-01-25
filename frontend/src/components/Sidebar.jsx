import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, Shield, Brain, Menu, Activity, X } from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';
import { Button } from './ui/button';

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const navItems = [
    { to: '/', icon: FileText, label: 'Briefing' },
    { to: '/command-center', icon: LayoutDashboard, label: 'Command Center' },
    { to: '/threat-intel', icon: Shield, label: 'Threat Intel' },
    { to: '/ai-logic', icon: Brain, label: 'AI Detection Logic' },
  ];

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar Container */}
      <aside className={`
        fixed top-0 left-0 z-50 h-full w-64 bg-card border-r border-border
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="h-full flex flex-col">
          {/* Logo Area */}
          <div className="h-16 flex items-center justify-between px-6 border-b border-border">
            <div className="flex items-center">
              <Activity className="w-6 h-6 text-primary mr-2" />
              <span className="text-lg font-display font-bold text-foreground">
                Sentinel<span className="text-primary">X</span>
              </span>
            </div>
            {/* Mobile Close Button */}
            <Button variant="ghost" size="icon" className="lg:hidden" onClick={toggleSidebar}>
              <X className="w-5 h-5" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 py-6 px-3 space-y-1 overflow-y-auto">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `
                  flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-all duration-200
                  ${isActive 
                    ? 'bg-primary/10 text-primary glow-cyan border-l-2 border-primary' 
                    : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
                  }
                `}
                onClick={() => window.innerWidth < 1024 && toggleSidebar()}
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.label}
              </NavLink>
            ))}
          </nav>

          {/* Footer Area */}
          <div className="p-4 border-t border-border">
            <div className="flex items-center justify-between mb-4">
               <span className="text-xs font-semibold text-muted-foreground">THEME</span>
               <ThemeToggle />
            </div>
            
            <div className="bg-secondary/50 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                <span className="text-xs font-mono text-muted-foreground">SYSTEM ONLINE</span>
              </div>
              <p className="text-[10px] text-muted-foreground/60">
                v2.1.0 Enterprise
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile Toggle Button */}
      <button
        onClick={toggleSidebar}
        className="fixed top-4 left-4 z-50 p-2 rounded-md bg-card border border-border lg:hidden"
      >
        <Menu className="w-6 h-6 text-foreground" />
      </button>
    </>
  );
};

export default Sidebar;
