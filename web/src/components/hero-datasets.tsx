'use client';

import { Database, TrendingUp, MapPin, AlertTriangle, Zap } from 'lucide-react';

const iconMap = {
  time_series: Database,
  line_chart: TrendingUp,
  heatmap: AlertTriangle,
  map: MapPin,
  bar_chart: Database,
  growth_chart: Zap,
};

const domainColors = {
  justice: 'text-sa-red',
  economy: 'text-federal-blue',
  infrastructure: 'text-slate-600 dark:text-slate-400',
  education: 'text-federal-blue',
  health: 'text-sa-red',
  environment: 'text-green-600 dark:text-green-500',
};

export function HeroDatasets() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <HeroCard
        id="sa-crime-statistics"
        name="SA Crime Statistics"
        description="Recorded crime by suburb, 2010-2026"
        domain="justice"
        vizType="time_series"
      />
      <HeroCard
        id="au-cost-of-living-cpi"
        name="Adelaide CPI"
        description="Consumer Price Index trends"
        domain="economy"
        vizType="line_chart"
      />
      <HeroCard
        id="sa-road-crash-data"
        name="SA Road Crashes"
        description="Crash locations and severity, 2020-2024"
        domain="infrastructure"
        vizType="heatmap"
      />
      <HeroCard
        id="sa-school-locations"
        name="SA School Locations"
        description="Government school and preschool sites"
        domain="education"
        vizType="map"
      />
      <HeroCard
        id="sa-health-ed-performance"
        name="ED Wait Times"
        description="Emergency department performance"
        domain="health"
        vizType="bar_chart"
      />
      <HeroCard
        id="au-small-scale-renewable-installations"
        name="Renewable Installations"
        description="Rooftop solar and battery installations"
        domain="environment"
        vizType="growth_chart"
      />
    </div>
  );
}

function HeroCard({
  name,
  description,
  domain,
  vizType,
}: {
  id: string;
  name: string;
  description: string;
  domain: keyof typeof domainColors;
  vizType: keyof typeof iconMap;
}) {
  const Icon = iconMap[vizType];
  const colorClass = domainColors[domain];

  return (
    <div className="group relative p-6 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-federal-blue dark:hover:border-federal-blue transition-all hover:shadow-lg">
      <div className="flex items-start gap-4">
        <div
          className={`p-2 rounded-lg bg-slate-100 dark:bg-slate-800 ${colorClass} group-hover:bg-federal-blue/10 dark:group-hover:bg-federal-blue/20 group-hover:text-federal-blue transition-colors`}
        >
          <Icon className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-1 group-hover:text-federal-blue transition-colors">
            {name}
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">{description}</p>
          <span className="inline-block text-xs font-medium text-slate-500 dark:text-slate-500 uppercase tracking-wide">
            {domain}
          </span>
        </div>
      </div>
    </div>
  );
}
