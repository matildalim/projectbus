import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface DataContextType {
  fleetData: any;
  currentScenario: any;
  scenarioType: 'fleet' | 'light' | 'optimal' | 'wasteful';
  setScenarioType: (type: 'fleet' | 'light' | 'optimal' | 'wasteful') => void;
  isLoading: boolean;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export function DataProvider({ children }: { children: ReactNode }) {
  const [fleetData, setFleetData] = useState<any>(null);
  const [currentScenario, setCurrentScenario] = useState<any>(null);
  const [scenarioType, setScenarioType] = useState<'fleet' | 'light' | 'optimal' | 'wasteful'>('fleet');
  const [isLoading, setIsLoading] = useState(true);

  // Load data based on scenario type
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        let dataPath = '';
        
        switch (scenarioType) {
          case 'fleet':
            dataPath = '/data/fleet_weekly_stats.json';
            break;
          case 'light':
            dataPath = '/data/scenario_light_load.json';
            break;
          case 'optimal':
            dataPath = '/data/scenario_heavy_optimal.json';
            break;
          case 'wasteful':
            dataPath = '/data/scenario_heavy_wasteful.json';
            break;
        }

        const response = await fetch(dataPath);
        const data = await response.json();
        
        if (scenarioType === 'fleet') {
          setFleetData(data);
          setCurrentScenario(null);
        } else {
          setCurrentScenario(data);
          // Still load fleet data for comparison
          if (!fleetData) {
            const fleetResponse = await fetch('/data/fleet_weekly_stats.json');
            const fleetJson = await fleetResponse.json();
            setFleetData(fleetJson);
          }
        }
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [scenarioType]);

  return (
    <DataContext.Provider value={{ fleetData, currentScenario, scenarioType, setScenarioType, isLoading }}>
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within DataProvider');
  }
  return context;
}