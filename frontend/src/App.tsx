import { useState } from 'react';
import { OperationsDashboard } from './components/operations-dashboard';
import { DriverDisplay } from './components/driver-display';
import { BarChart3, Gauge } from 'lucide-react';

export default function App() {
  const [activeInterface, setActiveInterface] = useState<'operations' | 'driver'>('operations');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Interface Switcher */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="max-w-7xl mx-auto flex gap-4">
          <button
            onClick={() => setActiveInterface('operations')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-colors ${
              activeInterface === 'operations'
                ? 'bg-blue-900 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <BarChart3 className="w-5 h-5" />
            Operations Dashboard
          </button>
          <button
            onClick={() => setActiveInterface('driver')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-colors ${
              activeInterface === 'driver'
                ? 'bg-blue-900 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Gauge className="w-5 h-5" />
            Driver Display
          </button>
        </div>
      </div>

      {/* Active Interface */}
      {activeInterface === 'operations' ? <OperationsDashboard /> : <DriverDisplay />}
    </div>
  );
}
