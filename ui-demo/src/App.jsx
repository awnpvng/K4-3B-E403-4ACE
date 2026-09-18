import { useEffect, useMemo, useState } from 'react';
import {
  Activity,
  ArrowUpDown,
  CalendarDays,
  Check,
  CircleAlert,
  Clock3,
  Copy,
  ExternalLink,
  Filter,
  LayoutDashboard,
  MessageSquareText,
  Play,
  Settings,
  Sparkles,
  TrendingUp,
  Trophy,
} from 'lucide-react';
import statsData from '../../output/stats.json';
import questionsCsv from '../../output/questions_analyzed.csv?raw';

const splitCsvLine = (line) => {
  const values = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];

    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      values.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }

  values.push(current.trim());
  return values;
};

const parseCsv = (csvText) => {
  if (!csvText) return [];

  const rows = csvText.trim().split(/\r?\n/);
  if (rows.length < 2) return [];

  const headers = splitCsvLine(rows[0]);

  return rows.slice(1).filter(Boolean).map((row) => {
    const values = splitCsvLine(row);
    const record = {};

    headers.forEach((header, index) => {
      record[header] = values[index] ?? '';
    });

    return record;
  });
};

const normalizeQuestion = (row) => {
  const msgId = row.msg_id || 'unknown';
  const questionText = row.content_clean || row.content || 'No content';
  const intent = (row.intent || 'other').toLowerCase();
  const status = (row.status || 'unknown').toLowerCase();
  const priority = Number(row.priority_score || 0);
  const repeats = Number(row.cluster_size || 1);
  const ageHours = Number(row.age_hours || 0);

  return {
    id: msgId,
    intent,
    status,
    question: questionText,
    priority,
    repeats,
    cluster: row.cluster_id || 'cluster_unknown',
    postedAt: row.created_at_vn || new Date().toISOString(),
    link: `https://discord.com/msg/${msgId}`,
    ageHours,
    representative: row.representative || questionText,
    reason: status === 'unanswered'
      ? 'Question still requires a human answer and has not been resolved in the recent thread.'
      : 'Question has been processed by the pipeline and classified for TA follow-up.',
  };
};

const rawQuestions = parseCsv(questionsCsv).map(normalizeQuestion);

const kpiBase = [
  { label: 'Total messages', value: statsData.total_messages, trend: 'from current run' },
  { label: 'Questions', value: statsData.total_questions, trend: 'filtered and classified' },
  { label: 'Answered', value: statsData.answered, trend: 'resolved within thread' },
  { label: 'Unanswered', value: statsData.unanswered, trend: 'needs follow-up' },
  { label: 'Clusters', value: statsData.clusters, trend: 'similar-answer groups' },
];

const navItems = [
  { label: '# general', value: 'general', icon: MessageSquareText },
  { label: '# ta-ops', value: 'ta-ops', icon: LayoutDashboard },
  { label: '# qna-alerts', value: 'qna-alerts', icon: CircleAlert },
  { label: '# bot-commands', value: 'bot-commands', icon: Sparkles },
];

const commandHelp = [
  '/leaderboard — bảng xếp hạng câu hỏi ưu tiên',
  '/unanswered — danh sách câu hỏi chưa trả lời > 4h',
  '/trend — xu hướng chủ đề hot',
  '/dashboard — KPI tổng quan',
  '/help — hiển thị trợ giúp',
];

const intentClasses = {
  support: 'bg-indigo-100 text-indigo-700',
  team: 'bg-amber-100 text-amber-700',
  other: 'bg-slate-100 text-slate-700',
  default: 'bg-slate-100 text-slate-700',
};

const statusClasses = {
  unanswered: 'bg-rose-100 text-rose-700',
  answered: 'bg-emerald-100 text-emerald-700',
  other: 'bg-slate-100 text-slate-700',
};

const levelClasses = {
  High: 'bg-rose-100 text-rose-700',
  Medium: 'bg-amber-100 text-amber-700',
  Low: 'bg-emerald-100 text-emerald-700',
};

function DataFrameTable({ columns, rows, className = '' }) {
  return (
    <div className={`overflow-hidden rounded-xl border border-slate-200 bg-slate-950 text-left shadow-xl ${className}`}>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm text-slate-100">
          <thead className="bg-slate-900">
            <tr>
              {columns.map((column) => (
                <th key={column} className="border-b border-slate-700 px-3 py-2.5 font-semibold tracking-wide text-slate-300">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={`${row[0] || 'row'}-${index}`} className={index % 2 === 0 ? 'bg-slate-950/80' : 'bg-slate-900/70'}>
                {row.map((cell, cellIndex) => (
                  <td key={`${cell}-${cellIndex}`} className="border-b border-slate-800 px-3 py-2.5 align-top text-slate-200">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function App() {
  const [selectedIntent, setSelectedIntent] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [sortBy, setSortBy] = useState('priority');
  const [searchTerm, setSearchTerm] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [activeView, setActiveView] = useState('bot-commands');
  const [selectedQuestion, setSelectedQuestion] = useState(rawQuestions[0] ?? null);
  const [copiedId, setCopiedId] = useState(null);
  const [draft, setDraft] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      author: 'TA Bot',
      role: 'bot',
      content: 'Chào mừng bạn đến Discord Q&A Console. Gõ /help để xem lệnh có sẵn.',
      type: 'text',
    },
  ]);

  const intentOptions = useMemo(
    () => ['all', ...new Set(rawQuestions.map((item) => item.intent).filter(Boolean))],
    []
  );

  const statusOptions = useMemo(
    () => ['all', ...new Set(rawQuestions.map((item) => item.status).filter(Boolean))],
    []
  );

  const filteredLeaderboard = useMemo(() => {
    let result = [...rawQuestions];

    if (searchTerm.trim()) {
      const query = searchTerm.trim().toLowerCase();
      result = result.filter(
        (item) =>
          item.question.toLowerCase().includes(query) ||
          item.intent.toLowerCase().includes(query)
      );
    }

    if (selectedIntent !== 'all') {
      result = result.filter((item) => item.intent === selectedIntent);
    }

    if (selectedStatus !== 'all') {
      result = result.filter((item) => item.status === selectedStatus);
    }

    if (sortBy === 'priority') {
      result.sort((a, b) => b.priority - a.priority);
    }

    if (sortBy === 'newest') {
      result.sort((a, b) => new Date(b.postedAt) - new Date(a.postedAt));
    }

    if (sortBy === 'repeated') {
      result.sort((a, b) => b.repeats - a.repeats);
    }

    return result.map((item, index) => ({ ...item, rank: index + 1 }));
  }, [searchTerm, selectedIntent, selectedStatus, sortBy]);

  useEffect(() => {
    if (filteredLeaderboard.length > 0) {
      setSelectedQuestion((previous) => {
        const exists = filteredLeaderboard.some((item) => item.id === previous?.id);
        return exists ? previous : filteredLeaderboard[0];
      });
    }
  }, [filteredLeaderboard]);

  const trendData = useMemo(() => {
    const map = new Map();

    rawQuestions.forEach((item) => {
      if (!map.has(item.intent)) {
        map.set(item.intent, { name: item.intent, count: 0, total: 0 });
      }

      const current = map.get(item.intent);
      current.count += 1;
      current.total += item.priority;
    });

    return [...map.values()]
      .map((item) => ({
        name: item.name,
        count: item.count,
        score: Number((item.total / item.count).toFixed(1)),
        level: item.total / item.count >= 2.5 ? 'High' : item.total / item.count >= 1.5 ? 'Medium' : 'Low',
      }))
      .sort((a, b) => b.count - a.count);
  }, []);

  const unansweredQuestions = useMemo(
    () =>
      rawQuestions
        .filter((item) => item.status === 'unanswered')
        .slice(0, 5)
        .map((item) => ({
          ...item,
          stale: `${Math.max(1, Math.round(item.ageHours || 4))}h`,
        })),
    []
  );

  const formattedDate = useMemo(
    () =>
      new Intl.DateTimeFormat('en-GB', {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      }).format(new Date()),
    []
  );

  const handleRunAnalysis = () => {
    setIsRunning(true);
    setTimeout(() => setIsRunning(false), 1200);
  };

  const handleCopy = async (id, value) => {
    try {
      await navigator.clipboard.writeText(value);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 1200);
    } catch (error) {
      console.error('Copy failed', error);
    }
  };

  const leaderboardRows = filteredLeaderboard.slice(0, 8).map((item) => [
    `#${item.rank}`,
    item.priority.toFixed(1),
    item.intent,
    item.status,
    item.question.length > 60 ? `${item.question.slice(0, 60)}...` : item.question,
  ]);

  const unansweredRows = unansweredQuestions.map((item) => [
    item.intent,
    item.stale,
    item.question.length > 75 ? `${item.question.slice(0, 75)}...` : item.question,
  ]);

  const trendRows = trendData.map((item) => [
    item.name,
    String(item.count),
    item.score,
    item.level,
  ]);

  const handleSendCommand = () => {
    const trimmed = draft.trim();
    if (!trimmed) return;

    const userMessage = {
      id: Date.now(),
      author: 'You',
      role: 'user',
      content: trimmed,
      type: 'text',
    };

    const command = trimmed.toLowerCase();
    const reply = { id: Date.now() + 1, author: 'TA Bot', role: 'bot' };

    if (command === '/leaderboard') {
      reply.type = 'table';
      reply.title = 'Leaderboard';
      reply.columns = ['Rank', 'Priority', 'Intent', 'Status', 'Question'];
      reply.rows = leaderboardRows;
      setActiveView('bot-commands');
    } else if (command === '/unanswered') {
      reply.type = 'table';
      reply.title = 'Unanswered > 4h';
      reply.columns = ['Intent', 'Stale', 'Question'];
      reply.rows = unansweredRows;
      setActiveView('bot-commands');
    } else if (command === '/trend') {
      reply.type = 'table';
      reply.title = 'Trend';
      reply.columns = ['Intent', 'Questions', 'Avg Priority', 'Level'];
      reply.rows = trendRows;
      setActiveView('bot-commands');
    } else if (command === '/dashboard') {
      reply.type = 'summary';
      reply.title = 'System Summary';
      reply.content = `${statsData.total_questions} câu hỏi • ${statsData.answered} answered • ${statsData.unanswered} unanswered • ${statsData.clusters} clusters`;
      setActiveView('bot-commands');
    } else if (command === '/help') {
      reply.type = 'help';
      reply.title = 'Bot Commands';
      reply.content = commandHelp.join('\n');
      setActiveView('bot-commands');
    } else {
      reply.type = 'text';
      reply.content = `Lệnh không hợp lệ: ${trimmed}. Gõ /help để xem danh sách lệnh có sẵn.`;
    }

    setMessages((prev) => [...prev, userMessage, reply]);
    setDraft('');
  };

  const renderDiscordView = () => (
    <div className="grid gap-6 xl:grid-cols-[220px_minmax(0,1fr)_320px]">
      <aside className="rounded-2xl border border-slate-200 bg-slate-950 p-4 text-slate-200 shadow-soft">
        <div className="mb-5 flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500 font-bold text-white">
            TA
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.15em] text-slate-400">Server</div>
            <div className="font-semibold">LabCoach</div>
          </div>
        </div>

        <div className="space-y-2">
          {navItems.map(({ label, value, icon: Icon }) => (
            <button
              key={label}
              type="button"
              onClick={() => setActiveView(value)}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left text-sm transition ${
                activeView === value
                  ? 'bg-slate-800 text-white'
                  : 'text-slate-300 hover:bg-slate-900 hover:text-white'
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>
      </aside>

      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-5 py-3">
          <div>
            <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Channel</div>
            <div className="text-sm font-semibold text-slate-800"># bot-commands</div>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold text-emerald-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Online
          </div>
        </div>

        <div className="flex h-[520px] flex-col overflow-y-auto bg-white p-4">
          {messages.map((message) => (
            <div key={message.id} className={`mb-4 flex gap-3 ${message.role === 'user' ? 'justify-end' : ''}`}>
              {message.role === 'bot' && (
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-100 font-bold text-indigo-700">
                  B
                </div>
              )}

              <div className={`${message.role === 'user' ? 'max-w-[75%]' : 'max-w-[85%]'}`}>
                <div className={`mb-1 text-xs font-medium ${message.role === 'user' ? 'text-right text-slate-500' : 'text-slate-500'}`}>
                  {message.author}
                </div>

                {message.type === 'table' ? (
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3">
                    <div className="mb-2 text-sm font-semibold text-slate-800">{message.title}</div>
                    <DataFrameTable columns={message.columns} rows={message.rows} className="max-h-[320px]" />
                  </div>
                ) : message.type === 'summary' ? (
                  <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-4 text-sm text-slate-700">
                    <div className="mb-2 font-semibold text-indigo-700">{message.title}</div>
                    <div>{message.content}</div>
                  </div>
                ) : message.type === 'help' ? (
                  <div className="rounded-2xl border border-violet-200 bg-violet-50 p-4 text-sm text-slate-700">
                    <div className="mb-2 font-semibold text-violet-700">{message.title}</div>
                    <pre className="whitespace-pre-line font-mono text-xs leading-6 text-slate-700">{message.content}</pre>
                  </div>
                ) : (
                  <div className={`rounded-2xl px-4 py-3 text-sm leading-6 ${message.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700'}`}>
                    {message.content}
                  </div>
                )}
              </div>

              {message.role === 'user' && (
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 font-bold text-slate-700">
                  U
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="border-t border-slate-200 bg-slate-50 p-3">
          <div className="mb-2 flex flex-wrap gap-2">
            {commandHelp.map((command) => (
              <button
                key={command}
                type="button"
                onClick={() => setDraft(command.split('—')[0].trim())}
                className="rounded-full border border-indigo-200 bg-white px-2.5 py-1 text-[11px] font-medium text-indigo-700 hover:bg-indigo-50"
              >
                {command.split('—')[0].trim()}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-3 py-2">
            <span className="text-lg text-indigo-600">/</span>
            <input
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') handleSendCommand();
              }}
              placeholder="Nhập lệnh, ví dụ /leaderboard"
              className="flex-1 border-0 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
            />
            <button
              type="button"
              onClick={handleSendCommand}
              className="rounded-xl bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
            >
              Send
            </button>
          </div>
        </div>
      </section>

      <aside className="space-y-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
        <div>
          <div className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">System health</div>
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
            Pipeline đang chạy ổn định
          </div>
        </div>

        <div>
          <div className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">Quick stats</div>
          <div className="space-y-2 text-sm text-slate-700">
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-2.5"><span>Total messages</span><strong>{statsData.total_messages}</strong></div>
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-2.5"><span>Questions</span><strong>{statsData.total_questions}</strong></div>
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-2.5"><span>Answered</span><strong>{statsData.answered}</strong></div>
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-2.5"><span>Unanswered</span><strong>{statsData.unanswered}</strong></div>
          </div>
        </div>

        <div>
          <div className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">AI workflow</div>
          <div className="space-y-2 text-sm text-slate-600">
            <div className="rounded-xl bg-slate-50 p-2">Discord Messages → Parse & Filter</div>
            <div className="rounded-xl bg-slate-50 p-2">Intent Classification</div>
            <div className="rounded-xl bg-slate-50 p-2">Clustering</div>
            <div className="rounded-xl bg-slate-50 p-2">Detection & Scoring</div>
          </div>
        </div>
      </aside>
    </div>
  );

  const renderBody = () => {
    if (activeView === 'general' || activeView === 'ta-ops' || activeView === 'qna-alerts' || activeView === 'bot-commands') {
      return renderDiscordView();
    }

    if (activeView === 'leaderboard') {
      return (
        <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Trophy className="h-5 w-5 text-indigo-600" />
              <h2 className="text-lg font-semibold text-slate-900">Leaderboard</h2>
            </div>
            <button
              type="button"
              onClick={() => setDraft('/leaderboard')}
              className="rounded-xl bg-indigo-600 px-3 py-2 text-sm font-semibold text-white"
            >
              Run /leaderboard
            </button>
          </div>
          <DataFrameTable columns={['Rank', 'Priority', 'Intent', 'Status', 'Question']} rows={leaderboardRows} />
        </section>
      );
    }

    if (activeView === 'unanswered') {
      return (
        <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CircleAlert className="h-5 w-5 text-rose-600" />
              <h2 className="text-lg font-semibold text-slate-900">Unanswered</h2>
            </div>
            <button
              type="button"
              onClick={() => setDraft('/unanswered')}
              className="rounded-xl bg-rose-600 px-3 py-2 text-sm font-semibold text-white"
            >
              Run /unanswered
            </button>
          </div>
          <DataFrameTable columns={['Intent', 'Stale', 'Question']} rows={unansweredRows} />
        </section>
      );
    }

    if (activeView === 'trend') {
      return (
        <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-indigo-600" />
              <h2 className="text-lg font-semibold text-slate-900">Trend</h2>
            </div>
            <button
              type="button"
              onClick={() => setDraft('/trend')}
              className="rounded-xl bg-indigo-600 px-3 py-2 text-sm font-semibold text-white"
            >
              Run /trend
            </button>
          </div>
          <DataFrameTable columns={['Intent', 'Questions', 'Avg Priority', 'Level']} rows={trendRows} />
        </section>
      );
    }

    return (
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft">
        <h2 className="text-lg font-semibold text-slate-900">Settings</h2>
        <p className="mt-3 text-sm text-slate-600">This panel is reserved for pipeline configuration and alert preferences.</p>
      </section>
    );
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="flex min-h-screen">
        <main className="flex-1 p-4 md:p-6">
          <header className="mb-6 flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-soft md:flex-row md:items-center md:justify-between">
            <div>
              <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Discord Q&A bot</div>
              <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-900 md:text-3xl">LabCoach Intelligence Console</h1>
            </div>

            <div className="flex items-center gap-3">
              <div className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600">
                <CalendarDays className="h-4 w-4 text-indigo-600" />
                {formattedDate}
              </div>

              <button
                type="button"
                onClick={handleRunAnalysis}
                className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-indigo-400"
                disabled={isRunning}
              >
                {isRunning ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Run Analysis
                  </>
                )}
              </button>
            </div>
          </header>

          {renderBody()}
        </main>
      </div>
    </div>
  );
}

export default App;
