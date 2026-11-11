import { useQuery } from '@tanstack/react-query';
import { fetchApi } from '../lib/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const { data: challenges } = useQuery({ queryKey: ['challenges'], queryFn: () => fetchApi('/challenges/') });

  const chartData = [
    { name: 'Passed', count: 45 },
    { name: 'Failed', count: 12 },
    { name: 'Invalid', count: 3 },
  ];

  return (
    <div className="container">
      <h1>Analytics Dashboard</h1>
      <div className="grid">
        <div className="card">
          <h3>Evaluation Results</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#8b949e" />
              <YAxis stroke="#8b949e" />
              <Tooltip contentStyle={{ backgroundColor: '#161b22', borderColor: '#30363d' }} />
              <Bar dataKey="count" fill="#58a6ff" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h3>Active Challenges ({challenges?.length || 0})</h3>
          <ul>
            {challenges?.map((c: any) => (
              <li key={c.id}>{c.title} ({c.difficulty})</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}