import React from 'react';
import { ViewState } from '../types';
import { Button } from './ui/button';
import { Shield } from 'lucide-react';

interface HeaderProps {
  currentView: ViewState;
  onChangeView: (view: ViewState) => void;
}

const Header: React.FC<HeaderProps> = ({ currentView, onChangeView }) => {
  const navItems: { id: ViewState; label: string }[] = [
    { id: 'overview', label: 'Dashboard' },
    { id: 'disputes', label: 'Disputes' },
    { id: 'agent-studio', label: 'Agent Studio' },
    { id: 'automations', label: 'Automations' },
    { id: 'integrations', label: 'Integrations' },
  ];

  return (
    <header className="bg-background border-b sticky top-0 z-50">
      <div className="max-w-[2000px] mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo & Nav */}
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-primary rounded-lg flex items-center justify-center">
              <Shield className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="font-bold text-foreground text-xl tracking-tight">ChargeGuard</span>
            <span className="text-muted-foreground text-sm">|</span>
            <span className="font-bold text-xl">Huel</span>
          </div>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <div key={item.id} className="relative">
                <Button
                  onClick={() => onChangeView(item.id)}
                  variant={currentView === item.id ? "secondary" : "ghost"}
                  size="sm"
                  className="font-medium"
                >
                  {item.label}
                </Button>
                {currentView === item.id && (
                  <div className="absolute bottom-0 left-2 right-2 h-1 bg-blue-500 rounded-full" />
                )}
              </div>
            ))}
          </nav>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          <Button size="icon" variant="outline" className="rounded-full">
            <span className="font-bold text-sm">H</span>
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;