declare module 'react-plotly.js' {
  import { PlotData, Layout } from 'plotly.js';
  
  interface PlotProps {
    data: Partial<PlotData>[];
    layout?: Partial<Layout>;
    [key: string]: any;
  }
  
  const Plot: React.ComponentType<PlotProps>;
  export default Plot;
} 