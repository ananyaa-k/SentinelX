import React from 'react';
import { useLocation } from 'react-router-dom';
import { Bell, Search, User } from 'lucide-react';
import { Button } from '../ui/button';
import { ThemeToggle } from '../ThemeToggle';

const Header = ({ toggleSidebar }) => {
  const location = useLocation();

  const getPageTitle = (pathname) => {
    switch (pathname) {
      case '/':
        return 'Mission Briefing';
      case '/command-center':
        return 'Command Center';
      case '/threat-intel':
        return 'Threat Intelligence';
      case '/ai-logic':
        return 'Detection Pipeline';
      default:
        return 'SentinelX';
    }
  };

  return (
    <header className="h-16 border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-30 px-6 flex items-center justify-between">
      <div className="flex items-center gap-4">
        {/* Title (Hidden on mobile as it's in sidebar/menu) */}
        <h2 className="text-xl font-display font-bold text-foreground hidden md:block">
          {getPageTitle(location.pathname)}
        </h2>
      </div>

      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-primary">
          <Bell className="w-5 h-5" />
        </Button>
        <div className="h-8 w-8 rounded-full bg-secondary border border-border flex items-center justify-center">
           <User className="w-4 h-4 text-muted-foreground" />
        </div>
      </div>
    </header>
  );
};

export default Header;
