import { useState, useMemo } from "react";

// ═══════════════════════════════════════════════════════════
//  CONSTANTS & MOCK DATA
// ═══════════════════════════════════════════════════════════
const DAYS = ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba"];
const PERIODS = [
  { num:1, time:"08:00–08:45" },
  { num:2, time:"09:00–09:45" },
  { num:3, time:"10:00–10:45" },
  { num:4, time:"11:00–11:45" },
  { num:5, time:"12:30–13:15" },
  { num:6, time:"13:30–14:15" },
  { num:7, time:"14:30–15:15" },
];
const GRADES = [5,6,7,8,9,10,11];
const SECTIONS = ["A","B","C"];
const ALL_CLASSES = GRADES.flatMap(g => SECTIONS.map(s => `${g}-${s}`));

const SUBJ_COLORS = {
  "Matematika":  ["#EEF2FF","#4338CA","#A5B4FC"],
  "Fizika":      ["#F0FDF4","#15803D","#86EFAC"],
  "Kimyo":       ["#FFF7ED","#C2410C","#FDBA74"],
  "Biologiya":   ["#FDF4FF","#7E22CE","#D8B4FE"],
  "Tarix":       ["#FEFCE8","#A16207","#FDE047"],
  "Adabiyot":    ["#FFF1F2","#BE123C","#FECDD3"],
  "Geografiya":  ["#F0F9FF","#0369A1","#7DD3FC"],
  "Ingliz tili": ["#F0FDFA","#0F766E","#5EEAD4"],
  "Informatika": ["#F5F3FF","#6D28D9","#C4B5FD"],
  "Ona tili":    ["#FFF8F0","#D97706","#FCD34D"],
  "Jismoniy":    ["#F0FDF4","#166534","#4ADE80"],
  "Musiqa":      ["#FDF2F8","#9D174D","#F9A8D4"],
};

const initSubjects = [
  { id:1, name:"Matematika",  weeklyHours:5, code:"MATH" },
  { id:2, name:"Fizika",      weeklyHours:3, code:"PHYS" },
  { id:3, name:"Kimyo",       weeklyHours:3, code:"CHEM" },
  { id:4, name:"Biologiya",   weeklyHours:2, code:"BIO"  },
  { id:5, name:"Tarix",       weeklyHours:2, code:"HIST" },
  { id:6, name:"Adabiyot",    weeklyHours:3, code:"LIT"  },
  { id:7, name:"Ingliz tili", weeklyHours:4, code:"ENG"  },
  { id:8, name:"Informatika", weeklyHours:2, code:"IT"   },
];

const initTeachers = [
  { id:1, name:"Aliyev Bobur",     phone:"+998 90 123 45 67", email:"aliyev@maktab.uz",   subjects:[1,2], classes:["5-A","5-B","6-A","6-B","7-A"] },
  { id:2, name:"Karimov Sardor",   phone:"+998 91 234 56 78", email:"karimov@maktab.uz",  subjects:[1],   classes:["7-B","8-A","8-B","9-A","9-B"] },
  { id:3, name:"Rahimova Malika",  phone:"+998 93 345 67 89", email:"rahimova@maktab.uz", subjects:[3,4], classes:["5-A","6-A","7-A","8-A"] },
  { id:4, name:"Toshmatov Jasur",  phone:"+998 97 456 78 90", email:"toshmat@maktab.uz",  subjects:[5,6], classes:["8-A","8-B","9-A","9-B"] },
  { id:5, name:"Nazarova Dilnoza", phone:"+998 99 567 89 01", email:"nazarova@maktab.uz", subjects:[7],   classes:["5-A","5-B","6-A","6-B","7-A","7-B"] },
  { id:6, name:"Xolmatov Anvar",   phone:"+998 94 678 90 12", email:"xolmat@maktab.uz",   subjects:[8],   classes:["7-A","7-B","8-A","8-B","9-A"] },
];

const initRooms = [
  { id:1, name:"12-xona",     capacity:35, type:"oddiy"      },
  { id:2, name:"14-xona",     capacity:35, type:"oddiy"      },
  { id:3, name:"15-xona",     capacity:30, type:"oddiy"      },
  { id:4, name:"Fizika lab",  capacity:25, type:"laboratoriya" },
  { id:5, name:"Kimyo lab",   capacity:20, type:"laboratoriya" },
  { id:6, name:"Kompyuter",   capacity:30, type:"kompyuter"   },
  { id:7, name:"Sporzal",     capacity:60, type:"sport"       },
];

const initSchedule = [
  { id:1,  classId:"5-A", teacherId:1, subjectId:1, day:0, period:1, roomId:1 },
  { id:2,  classId:"5-B", teacherId:2, subjectId:1, day:0, period:1, roomId:2 },
  { id:3,  classId:"5-A", teacherId:3, subjectId:3, day:0, period:2, roomId:5 },
  { id:4,  classId:"6-A", teacherId:1, subjectId:2, day:1, period:1, roomId:4 },
  { id:5,  classId:"5-A", teacherId:4, subjectId:5, day:1, period:2, roomId:3 },
  { id:6,  classId:"7-A", teacherId:2, subjectId:1, day:2, period:3, roomId:1 },
  { id:7,  classId:"5-A", teacherId:5, subjectId:7, day:2, period:1, roomId:2 },
  { id:8,  classId:"6-A", teacherId:5, subjectId:7, day:3, period:2, roomId:2 },
  { id:9,  classId:"8-A", teacherId:4, subjectId:6, day:4, period:1, roomId:3 },
  { id:10, classId:"9-A", teacherId:6, subjectId:8, day:4, period:3, roomId:6 },
];

const initClasses = ALL_CLASSES.slice(0, 9).map((name, i) => ({
  id: i+1, name, grade: parseInt(name), section: name.split("-")[1],
  studentCount: Math.floor(Math.random()*8)+26,
  classTeacherId: [1,2,3,4,5,6][i % 6],
}));

// ═══════════════════════════════════════════════════════════
//  ICONS
// ═══════════════════════════════════════════════════════════
const I = ({ n, s=18 }) => {
  const p = { width:s, height:s, fill:"none", stroke:"currentColor", strokeWidth:"2", viewBox:"0 0 24 24", strokeLinecap:"round", strokeLinejoin:"round" };
  const icons = {
    home:     <svg {...p}><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>,
    users:    <svg {...p}><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
    book:     <svg {...p}><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>,
    calendar: <svg {...p}><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>,
    door:     <svg {...p}><path d="M3 3h18v18H3zM13 3v18M8 12h1"/></svg>,
    alert:    <svg {...p}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>,
    chart:    <svg {...p}><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>,
    grid:     <svg {...p}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>,
    plus:     <svg {...p}><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>,
    trash:    <svg {...p}><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>,
    edit:     <svg {...p}><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>,
    x:        <svg {...p}><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>,
    check:    <svg {...p}><polyline points="20 6 9 17 4 12"/></svg>,
    swap:     <svg {...p}><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>,
    print:    <svg {...p}><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>,
    info:     <svg {...p}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>,
    shield:   <svg {...p}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>,
    eye:      <svg {...p}><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>,
    user:     <svg {...p}><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>,
  };
  return icons[n] ?? null;
};

// ═══════════════════════════════════════════════════════════
//  HELPERS
// ═══════════════════════════════════════════════════════════
const uid = () => Date.now() + Math.random();
const sc = (name) => SUBJ_COLORS[name] || ["#F1F5F9","#475569","#CBD5E1"];

function getAvatarColor(id) {
  const colors = [
    ["#4338CA","#6366F1"], ["#0F766E","#14B8A6"], ["#B45309","#F59E0B"],
    ["#9D174D","#EC4899"], ["#065F46","#10B981"], ["#1E40AF","#3B82F6"],
  ];
  return colors[id % colors.length];
}

// ═══════════════════════════════════════════════════════════
//  SHARED UI
// ═══════════════════════════════════════════════════════════
function Modal({ title, width=540, onClose, children }) {
  return (
    <div onClick={onClose} style={{ position:"fixed",inset:0,background:"rgba(2,8,23,0.7)",backdropFilter:"blur(6px)",zIndex:1000,display:"flex",alignItems:"center",justifyContent:"center",padding:20 }}>
      <div onClick={e=>e.stopPropagation()} style={{ background:"#fff",borderRadius:24,width:"100%",maxWidth:width,boxShadow:"0 32px 80px rgba(0,0,0,0.22)",overflow:"hidden",animation:"modalIn .25s cubic-bezier(.34,1.56,.64,1)" }}>
        <div style={{ display:"flex",alignItems:"center",justifyContent:"space-between",padding:"22px 28px 18px",borderBottom:"1px solid #F1F5F9" }}>
          <span style={{ fontWeight:700,fontSize:17,color:"#0F172A",fontFamily:"'DM Sans',sans-serif" }}>{title}</span>
          <button onClick={onClose} style={{ background:"#F1F5F9",border:"none",borderRadius:10,width:34,height:34,cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",color:"#64748B" }}><I n="x" s={15}/></button>
        </div>
        <div style={{ padding:28 }}>{children}</div>
      </div>
    </div>
  );
}

function Btn({ children, variant="primary", size="md", onClick, icon, style={} }) {
  const base = { display:"flex",alignItems:"center",gap:7,border:"none",cursor:"pointer",fontFamily:"'DM Sans',sans-serif",fontWeight:600,borderRadius:11,transition:"all .15s" };
  const sizes = { sm:{padding:"7px 14px",fontSize:12}, md:{padding:"10px 18px",fontSize:13}, lg:{padding:"13px 22px",fontSize:14} };
  const variants = {
    primary:  { background:"#0F172A",color:"#fff" },
    accent:   { background:"#0D9488",color:"#fff" },
    ghost:    { background:"#F1F5F9",color:"#475569" },
    danger:   { background:"#FEF2F2",color:"#DC2626" },
    outline:  { background:"transparent",color:"#0F172A",border:"1.5px solid #E2E8F0" },
  };
  return (
    <button onClick={onClick} style={{ ...base,...sizes[size],...variants[variant],...style }}>
      {icon && <I n={icon} s={14}/>}{children}
    </button>
  );
}

function Tag({ children, color="#F1F5F9", text="#475569", border="#E2E8F0" }) {
  return <span style={{ background:color,color:text,border:`1px solid ${border}`,borderRadius:8,padding:"3px 10px",fontSize:12,fontWeight:600,whiteSpace:"nowrap" }}>{children}</span>;
}

function Input({ label, ...props }) {
  return (
    <div>
      {label && <label style={{ fontSize:12,fontWeight:600,color:"#64748B",display:"block",marginBottom:6,textTransform:"uppercase",letterSpacing:.5 }}>{label}</label>}
      <input {...props} style={{ width:"100%",padding:"11px 14px",border:"1.5px solid #E2E8F0",borderRadius:10,fontSize:14,color:"#0F172A",fontFamily:"'DM Sans',sans-serif",outline:"none",...(props.style||{}) }} />
    </div>
  );
}

function Select({ label, children, ...props }) {
  return (
    <div>
      {label && <label style={{ fontSize:12,fontWeight:600,color:"#64748B",display:"block",marginBottom:6,textTransform:"uppercase",letterSpacing:.5 }}>{label}</label>}
      <select {...props} style={{ width:"100%",padding:"11px 14px",border:"1.5px solid #E2E8F0",borderRadius:10,fontSize:14,color:"#0F172A",background:"#fff",fontFamily:"'DM Sans',sans-serif",outline:"none" }}>
        {children}
      </select>
    </div>
  );
}

function StatCard({ label, value, sub, color="#0D9488", icon }) {
  return (
    <div style={{ background:"#fff",borderRadius:20,padding:24,boxShadow:"0 1px 10px rgba(0,0,0,0.06)",border:"1px solid #F1F5F9" }}>
      <div style={{ display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:16 }}>
        <div style={{ width:44,height:44,borderRadius:14,background:color+"18",display:"flex",alignItems:"center",justifyContent:"center",color }}><I n={icon} s={20}/></div>
      </div>
      <div style={{ fontSize:32,fontWeight:800,color:"#0F172A",lineHeight:1,marginBottom:4 }}>{value}</div>
      <div style={{ fontSize:13,color:"#64748B",fontWeight:500 }}>{label}</div>
      {sub && <div style={{ fontSize:11,color:"#94A3B8",marginTop:4 }}>{sub}</div>}
    </div>
  );
}

function Avatar({ name, id, size=40 }) {
  const [from,to] = getAvatarColor(id);
  return (
    <div style={{ width:size,height:size,borderRadius:size*.35,background:`linear-gradient(135deg,${from},${to})`,display:"flex",alignItems:"center",justifyContent:"center",color:"#fff",fontWeight:700,fontSize:size*.38,flexShrink:0 }}>
      {name.charAt(0)}
    </div>
  );
}

function Toast({ toasts }) {
  return (
    <div style={{ position:"fixed",bottom:28,right:28,zIndex:9999,display:"flex",flexDirection:"column",gap:10 }}>
      {toasts.map(t=>(
        <div key={t.id} style={{ background:t.type==="error"?"#FEF2F2":"#F0FDF4",border:`1px solid ${t.type==="error"?"#FECACA":"#86EFAC"}`,color:t.type==="error"?"#DC2626":"#15803D",borderRadius:14,padding:"12px 18px",fontSize:13,fontWeight:600,display:"flex",alignItems:"center",gap:10,boxShadow:"0 8px 24px rgba(0,0,0,.12)",animation:"toastIn .3s ease",minWidth:280 }}>
          <I n={t.type==="error"?"alert":"check"} s={16}/>{t.msg}
        </div>
      ))}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  CONFLICT CHECKER
// ═══════════════════════════════════════════════════════════
function findConflicts(schedule, teachers, subjects, rooms) {
  const conflicts = [];
  for (let i=0; i<schedule.length; i++) {
    for (let j=i+1; j<schedule.length; j++) {
      const a=schedule[i], b=schedule[j];
      if (a.day !== b.day || a.period !== b.period) continue;
      if (a.classId === b.classId) {
        const sA = subjects.find(s=>s.id===a.subjectId)?.name;
        const sB = subjects.find(s=>s.id===b.subjectId)?.name;
        conflicts.push({ type:"class", msg:`${a.classId} sinfi ${DAYS[a.day]} ${a.period}-darsda 2 ta dars: ${sA} va ${sB}` });
      }
      if (a.teacherId === b.teacherId) {
        const t = teachers.find(t=>t.id===a.teacherId)?.name;
        conflicts.push({ type:"teacher", msg:`${t} — ${DAYS[a.day]} ${a.period}-darsda ${a.classId} va ${b.classId} da bir vaqtda` });
      }
      if (a.roomId && a.roomId === b.roomId) {
        const r = rooms.find(r=>r.id===a.roomId)?.name;
        conflicts.push({ type:"room", msg:`${r} — ${DAYS[a.day]} ${a.period}-darsda ${a.classId} va ${b.classId} band` });
      }
    }
  }
  return conflicts;
}

// ═══════════════════════════════════════════════════════════
//  MAIN APP
// ═══════════════════════════════════════════════════════════
export default function App() {
  const [page, setPage]         = useState("dashboard");
  const [teachers, setTeachers] = useState(initTeachers);
  const [subjects, setSubjects] = useState(initSubjects);
  const [rooms, setRooms]       = useState(initRooms);
  const [classes, setClasses]   = useState(initClasses);
  const [schedule, setSchedule] = useState(initSchedule);
  const [toasts, setToasts]     = useState([]);
  const [modal, setModal]       = useState(null);

  const toast = (msg, type="success") => {
    const id = uid();
    setToasts(t=>[...t,{id,msg,type}]);
    setTimeout(()=>setToasts(t=>t.filter(x=>x.id!==id)), 3200);
  };

  const conflicts = useMemo(() => findConflicts(schedule, teachers, subjects, rooms), [schedule,teachers,subjects,rooms]);

  const ctx = { teachers,setTeachers,subjects,setSubjects,rooms,setRooms,classes,setClasses,schedule,setSchedule,toast,setModal,conflicts };

  const NAV = [
    { id:"dashboard", label:"Dashboard",        icon:"home"     },
    { id:"teachers",  label:"O'qituvchilar",    icon:"users"    },
    { id:"subjects",  label:"Fanlar",           icon:"book"     },
    { id:"classes",   label:"Sinflar",          icon:"grid"     },
    { id:"rooms",     label:"Xonalar",          icon:"door"     },
    { id:"schedule",  label:"Haftalik Jadval",  icon:"calendar" },
    { id:"swap",      label:"Almashtirish",     icon:"swap"     },
    { id:"conflicts", label:"Konfliktlar",      icon:"alert",   badge: conflicts.length },
    { id:"report",    label:"Hisobot",          icon:"chart"    },
  ];

  return (
    <div style={{ display:"flex",height:"100vh",fontFamily:"'DM Sans',sans-serif",background:"#F6F8FA",overflow:"hidden" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap');
        *{box-sizing:border-box;margin:0;padding:0}
        input,select,button,textarea{font-family:'DM Sans',sans-serif}
        @keyframes modalIn{from{opacity:0;transform:scale(.94) translateY(12px)}to{opacity:1;transform:scale(1) translateY(0)}}
        @keyframes toastIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}
        @keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
        ::-webkit-scrollbar{width:5px;height:5px}
        ::-webkit-scrollbar-track{background:transparent}
        ::-webkit-scrollbar-thumb{background:#CBD5E1;border-radius:99px}
        input:focus,select:focus,textarea:focus{border-color:#0D9488!important;box-shadow:0 0 0 3px rgba(13,148,136,.12)}
      `}</style>

      {/* ── SIDEBAR ── */}
      <aside style={{ width:230,background:"#0F172A",display:"flex",flexDirection:"column",flexShrink:0 }}>
        {/* Logo */}
        <div style={{ padding:"24px 18px 20px" }}>
          <div style={{ background:"linear-gradient(135deg,#0D9488,#0F766E)",borderRadius:16,padding:"16px 18px" }}>
            <div style={{ fontSize:10,color:"rgba(255,255,255,.5)",fontWeight:700,letterSpacing:2,textTransform:"uppercase" }}>EduPlan Pro</div>
            <div style={{ fontSize:17,color:"#fff",fontWeight:800,marginTop:3 }}>Jadval Tizimi</div>
            <div style={{ fontSize:11,color:"rgba(255,255,255,.4)",marginTop:2 }}>2024–2025 o'quv yili</div>
          </div>
        </div>

        {/* Nav */}
        <nav style={{ flex:1,padding:"0 10px",overflowY:"auto" }}>
          {NAV.map(n => {
            const active = page === n.id;
            return (
              <button key={n.id} onClick={()=>setPage(n.id)} style={{
                width:"100%",display:"flex",alignItems:"center",gap:10,padding:"10px 12px",
                marginBottom:2,border:"none",borderRadius:12,cursor:"pointer",textAlign:"left",
                background: active ? "rgba(13,148,136,.18)" : "transparent",
                color: active ? "#2DD4BF" : "rgba(255,255,255,.45)",
                fontWeight: active ? 600 : 400, fontSize:13, transition:"all .15s",
                position:"relative",
              }}>
                <I n={n.icon} s={17}/>
                {n.label}
                {n.badge > 0 && (
                  <span style={{ position:"absolute",right:10,background:"#EF4444",color:"#fff",borderRadius:99,fontSize:10,fontWeight:700,padding:"1px 7px",minWidth:20,textAlign:"center" }}>
                    {n.badge}
                  </span>
                )}
                {active && <div style={{ position:"absolute",left:0,top:"50%",transform:"translateY(-50%)",width:3,height:20,background:"#0D9488",borderRadius:"0 3px 3px 0" }}/>}
              </button>
            );
          })}
        </nav>

        {/* Bottom info */}
        <div style={{ padding:"14px 18px 20px" }}>
          <div style={{ background:"rgba(255,255,255,.05)",borderRadius:12,padding:12 }}>
            <div style={{ fontSize:11,color:"rgba(255,255,255,.3)",marginBottom:4 }}>Jami o'quvchilar</div>
            <div style={{ fontSize:20,fontWeight:800,color:"#fff" }}>{classes.reduce((a,c)=>a+(c.studentCount||0),0)}</div>
            <div style={{ fontSize:11,color:"rgba(255,255,255,.3)",marginTop:2 }}>{classes.length} ta sinf</div>
          </div>
        </div>
      </aside>

      {/* ── MAIN ── */}
      <main style={{ flex:1,overflowY:"auto" }}>
        {page==="dashboard" && <Dashboard {...ctx}/>}
        {page==="teachers"  && <TeachersPage {...ctx}/>}
        {page==="subjects"  && <SubjectsPage {...ctx}/>}
        {page==="classes"   && <ClassesPage {...ctx}/>}
        {page==="rooms"     && <RoomsPage {...ctx}/>}
        {page==="schedule"  && <SchedulePage {...ctx}/>}
        {page==="swap"      && <SwapPage {...ctx}/>}
        {page==="conflicts" && <ConflictsPage {...ctx}/>}
        {page==="report"    && <ReportPage {...ctx}/>}
      </main>

      {/* ── MODALS ── */}
      {modal?.type==="assignSubject" && (
        <AssignSubjectModal {...modal} subjects={subjects} onClose={()=>setModal(null)}
          onSave={(tid,sids,cids)=>{ setTeachers(ts=>ts.map(t=>t.id===tid?{...t,subjects:sids,classes:cids}:t)); toast("Saqlandi ✅"); setModal(null); }}/>
      )}
      {modal?.type==="addEntry" && (
        <AddEntryModal {...modal} teachers={teachers} subjects={subjects} rooms={rooms} schedule={schedule}
          onSave={entry=>{ setSchedule(s=>[...s,{...entry,id:uid()}]); toast("Dars qo'shildi ✅"); setModal(null); }}
          onClose={()=>setModal(null)}/>
      )}
      {modal?.type==="viewEntry" && (
        <ViewEntryModal {...modal} teachers={teachers} subjects={subjects} rooms={rooms}
          onDelete={id=>{ setSchedule(s=>s.filter(x=>x.id!==id)); toast("O'chirildi","error"); setModal(null); }}
          onClose={()=>setModal(null)}/>
      )}

      <Toast toasts={toasts}/>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  DASHBOARD
// ═══════════════════════════════════════════════════════════
function Dashboard({ teachers, subjects, rooms, classes, schedule, conflicts, setPage }) {
  const weekFill = Math.round(schedule.length / (ALL_CLASSES.length * 6 * 7) * 100);
  return (
    <div style={{ padding:32 }}>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontSize:26,fontWeight:800,color:"#0F172A" }}>Xush kelibsiz! 👋</h1>
        <p style={{ color:"#64748B",marginTop:4 }}>Maktab jadval tizimining umumiy ko'rinishi</p>
      </div>

      {/* Conflict alert */}
      {conflicts.length > 0 && (
        <div style={{ background:"#FFF7ED",border:"1.5px solid #FED7AA",borderRadius:16,padding:"14px 18px",marginBottom:24,display:"flex",alignItems:"center",gap:12 }}>
          <div style={{ color:"#EA580C",flexShrink:0 }}><I n="alert" s={22}/></div>
          <div style={{ flex:1 }}>
            <div style={{ fontWeight:700,color:"#9A3412",fontSize:14 }}>Jadvalda {conflicts.length} ta konflikt aniqlandi!</div>
            <div style={{ color:"#C2410C",fontSize:13,marginTop:2 }}>Ziddiyatlarni ko'rish va bartaraf etish uchun "Konfliktlar" bo'limiga o'ting.</div>
          </div>
          <Btn variant="outline" size="sm" icon="eye" onClick={()=>setPage?.("conflicts")}>Ko'rish</Btn>
        </div>
      )}

      {/* Stats */}
      <div style={{ display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:16,marginBottom:24 }}>
        <StatCard label="O'qituvchilar" value={teachers.length} sub={`${subjects.length} ta fan`} color="#0D9488" icon="users"/>
        <StatCard label="Sinflar" value={classes.length} sub={`${classes.reduce((a,c)=>a+c.studentCount,0)} o'quvchi`} color="#6366F1" icon="grid"/>
        <StatCard label="Xonalar" value={rooms.length} sub="O'quv xonalari" color="#0EA5E9" icon="door"/>
        <StatCard label="Jadval to'ldirilgan" value={`${weekFill}%`} sub={`${schedule.length} ta dars joylashtirilgan`} color="#F59E0B" icon="calendar"/>
      </div>

      <div style={{ display:"grid",gridTemplateColumns:"2fr 1fr",gap:20 }}>
        {/* Teacher load */}
        <div style={{ background:"#fff",borderRadius:20,padding:24,boxShadow:"0 1px 10px rgba(0,0,0,.06)",border:"1px solid #F1F5F9" }}>
          <h3 style={{ fontSize:15,fontWeight:700,color:"#0F172A",marginBottom:18 }}>O'qituvchilar haftalik yuki</h3>
          {teachers.map(t=>{
            const cnt = schedule.filter(e=>e.teacherId===t.id).length;
            const pct = Math.min(cnt / 30 * 100, 100);
            const [from] = getAvatarColor(t.id);
            return (
              <div key={t.id} style={{ display:"flex",alignItems:"center",gap:12,marginBottom:14 }}>
                <Avatar name={t.name} id={t.id} size={34}/>
                <div style={{ flex:1 }}>
                  <div style={{ display:"flex",justifyContent:"space-between",marginBottom:5 }}>
                    <span style={{ fontSize:13,fontWeight:600,color:"#0F172A" }}>{t.name}</span>
                    <span style={{ fontSize:12,color:"#64748B" }}>{cnt}/30 soat</span>
                  </div>
                  <div style={{ height:6,background:"#F1F5F9",borderRadius:99,overflow:"hidden" }}>
                    <div style={{ height:"100%",width:`${pct}%`,background:from,borderRadius:99,transition:"width .6s ease" }}/>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick stats */}
        <div style={{ display:"flex",flexDirection:"column",gap:16 }}>
          <div style={{ background:"#0F172A",borderRadius:20,padding:22,color:"#fff" }}>
            <div style={{ fontSize:12,color:"rgba(255,255,255,.4)",fontWeight:600,marginBottom:8 }}>BUGUNGI DARSLAR</div>
            <div style={{ fontSize:36,fontWeight:800 }}>{schedule.filter(e=>e.day===0).length}</div>
            <div style={{ fontSize:13,color:"rgba(255,255,255,.5)",marginTop:4 }}>Dushanba bo'yicha</div>
          </div>
          <div style={{ background:"#fff",borderRadius:20,padding:22,boxShadow:"0 1px 10px rgba(0,0,0,.06)",border:"1px solid #F1F5F9" }}>
            <div style={{ fontSize:12,color:"#94A3B8",fontWeight:600,marginBottom:8 }}>FANLAR</div>
            <div style={{ display:"flex",flexWrap:"wrap",gap:6 }}>
              {subjects.slice(0,6).map(s=>{
                const [bg,,bd] = sc(s.name);
                const [,txt] = sc(s.name);
                return <Tag key={s.id} color={bg} text={txt} border={bd}>{s.name}</Tag>;
              })}
            </div>
          </div>
          <div style={{ background:"#F0FDFA",border:"1.5px solid #99F6E4",borderRadius:20,padding:22 }}>
            <div style={{ fontSize:12,color:"#0F766E",fontWeight:600,marginBottom:4 }}>Konfliktlar</div>
            <div style={{ fontSize:32,fontWeight:800,color:conflicts.length>0?"#EF4444":"#0D9488" }}>{conflicts.length}</div>
            <div style={{ fontSize:12,color:"#0F766E" }}>{conflicts.length===0?"Hammasi yaxshi ✅":"Hal qilish kerak!"}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  TEACHERS
// ═══════════════════════════════════════════════════════════
function TeachersPage({ teachers, setTeachers, subjects, schedule, toast, setModal }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name:"", phone:"", email:"" });
  const [search, setSearch] = useState("");

  const filtered = teachers.filter(t => t.name.toLowerCase().includes(search.toLowerCase()));

  const add = () => {
    if (!form.name.trim()) return toast("Ismni kiriting","error");
    setTeachers(ts=>[...ts,{ id:uid(), name:form.name, phone:form.phone, email:form.email, subjects:[], classes:[] }]);
    toast("O'qituvchi qo'shildi ✅");
    setForm({ name:"",phone:"",email:"" });
    setShowForm(false);
  };

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="O'qituvchilar" sub={`Jami ${teachers.length} ta o'qituvchi`}>
        <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Qidirish..." style={{ padding:"9px 14px",border:"1.5px solid #E2E8F0",borderRadius:10,fontSize:13,width:200,outline:"none" }}/>
        <Btn icon="plus" onClick={()=>setShowForm(v=>!v)}>Qo'shish</Btn>
      </PageHeader>

      {showForm && (
        <div style={{ background:"#fff",borderRadius:20,padding:24,marginBottom:20,border:"1.5px solid #CCFBF1",animation:"fadeUp .25s ease" }}>
          <div style={{ fontSize:14,fontWeight:700,color:"#0F172A",marginBottom:18 }}>Yangi o'qituvchi</div>
          <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:14,marginBottom:18 }}>
            <Input label="F.I.Sh *" value={form.name} onChange={e=>setForm(f=>({...f,name:e.target.value}))} placeholder="Aliyev Bobur"/>
            <Input label="Telefon" value={form.phone} onChange={e=>setForm(f=>({...f,phone:e.target.value}))} placeholder="+998 90 000 00 00"/>
            <Input label="Email" value={form.email} onChange={e=>setForm(f=>({...f,email:e.target.value}))} placeholder="email@maktab.uz"/>
          </div>
          <div style={{ display:"flex",gap:10 }}>
            <Btn onClick={add}>Saqlash</Btn>
            <Btn variant="ghost" onClick={()=>setShowForm(false)}>Bekor</Btn>
          </div>
        </div>
      )}

      <div style={{ display:"grid",gap:12 }}>
        {filtered.map(t=>{
          const load = schedule.filter(e=>e.teacherId===t.id).length;
          return (
            <div key={t.id} style={{ background:"#fff",borderRadius:18,padding:20,boxShadow:"0 1px 8px rgba(0,0,0,.05)",border:"1px solid #F1F5F9",display:"flex",alignItems:"center",gap:16,animation:"fadeUp .25s ease" }}>
              <Avatar name={t.name} id={t.id} size={48}/>
              <div style={{ flex:1,minWidth:0 }}>
                <div style={{ fontSize:15,fontWeight:700,color:"#0F172A" }}>{t.name}</div>
                <div style={{ fontSize:12,color:"#94A3B8",marginTop:2 }}>{t.phone} · {t.email}</div>
                <div style={{ display:"flex",flexWrap:"wrap",gap:5,marginTop:8 }}>
                  {t.subjects.length===0
                    ? <span style={{ fontSize:12,color:"#F59E0B",fontWeight:500 }}>⚠ Fan biriktirilmagan</span>
                    : t.subjects.map(sid=>{ const s=subjects.find(x=>x.id===sid); if(!s) return null; const [bg,tx,bd]=sc(s.name); return <Tag key={sid} color={bg} text={tx} border={bd}>{s.name}</Tag>; })}
                </div>
                {t.classes.length>0 && (
                  <div style={{ display:"flex",flexWrap:"wrap",gap:4,marginTop:6 }}>
                    {t.classes.map(c=><span key={c} style={{ fontSize:11,color:"#64748B",background:"#F8FAFC",border:"1px solid #E2E8F0",borderRadius:6,padding:"2px 7px" }}>{c}</span>)}
                  </div>
                )}
              </div>
              <div style={{ textAlign:"center",padding:"0 16px",borderLeft:"1px solid #F1F5F9",borderRight:"1px solid #F1F5F9",flexShrink:0 }}>
                <div style={{ fontSize:22,fontWeight:800,color:"#0D9488" }}>{load}</div>
                <div style={{ fontSize:11,color:"#94A3B8" }}>dars/hafta</div>
              </div>
              <div style={{ display:"flex",gap:8,flexShrink:0 }}>
                <Btn variant="outline" size="sm" icon="edit" onClick={()=>setModal({ type:"assignSubject", teacher:t })}>Fan biriktir</Btn>
                <Btn variant="danger" size="sm" icon="trash" onClick={()=>{ setTeachers(ts=>ts.filter(x=>x.id!==t.id)); toast("O'chirildi","error"); }}/>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  SUBJECTS
// ═══════════════════════════════════════════════════════════
function SubjectsPage({ subjects, setSubjects, teachers, schedule, toast }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name:"", weeklyHours:3, code:"" });

  const add = () => {
    if (!form.name.trim()) return toast("Fan nomini kiriting","error");
    setSubjects(ss=>[...ss,{ id:uid(), name:form.name, weeklyHours:+form.weeklyHours, code:form.code }]);
    toast("Fan qo'shildi ✅");
    setForm({ name:"",weeklyHours:3,code:"" });
    setShowForm(false);
  };

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="Fanlar" sub={`${subjects.length} ta o'quv fani`}>
        <Btn icon="plus" onClick={()=>setShowForm(v=>!v)}>Fan qo'shish</Btn>
      </PageHeader>

      {showForm && (
        <div style={{ background:"#fff",borderRadius:20,padding:24,marginBottom:20,border:"1.5px solid #CCFBF1",animation:"fadeUp .25s ease" }}>
          <div style={{ fontSize:14,fontWeight:700,color:"#0F172A",marginBottom:18 }}>Yangi fan</div>
          <div style={{ display:"grid",gridTemplateColumns:"2fr 1fr 1fr",gap:14,marginBottom:18 }}>
            <Input label="Fan nomi *" value={form.name} onChange={e=>setForm(f=>({...f,name:e.target.value}))} placeholder="Matematika"/>
            <Input label="Kod" value={form.code} onChange={e=>setForm(f=>({...f,code:e.target.value}))} placeholder="MATH"/>
            <Input label="Haftalik soat" type="number" min="1" max="10" value={form.weeklyHours} onChange={e=>setForm(f=>({...f,weeklyHours:e.target.value}))}/>
          </div>
          <div style={{ display:"flex",gap:10 }}>
            <Btn onClick={add}>Saqlash</Btn>
            <Btn variant="ghost" onClick={()=>setShowForm(false)}>Bekor</Btn>
          </div>
        </div>
      )}

      <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:16 }}>
        {subjects.map(s=>{
          const [bg,tx,bd] = sc(s.name);
          const teacherCount = teachers.filter(t=>t.subjects.includes(s.id)).length;
          const lessonsCount = schedule.filter(e=>e.subjectId===s.id).length;
          return (
            <div key={s.id} style={{ background:"#fff",borderRadius:20,padding:22,boxShadow:"0 1px 8px rgba(0,0,0,.05)",border:"1px solid #F1F5F9",animation:"fadeUp .25s ease" }}>
              <div style={{ display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:16 }}>
                <div style={{ width:48,height:48,borderRadius:14,background:bg,border:`1.5px solid ${bd}`,display:"flex",alignItems:"center",justifyContent:"center",color:tx,fontWeight:800,fontSize:14 }}>
                  {s.code || s.name.slice(0,3).toUpperCase()}
                </div>
                <button onClick={()=>setSubjects(ss=>ss.filter(x=>x.id!==s.id))} style={{ background:"#FEF2F2",border:"none",borderRadius:8,width:30,height:30,cursor:"pointer",color:"#EF4444",display:"flex",alignItems:"center",justifyContent:"center" }}>
                  <I n="trash" s={13}/>
                </button>
              </div>
              <div style={{ fontSize:16,fontWeight:700,color:"#0F172A",marginBottom:4 }}>{s.name}</div>
              <div style={{ fontSize:13,color:"#64748B",marginBottom:14 }}>Haftada <span style={{ color:tx,fontWeight:700 }}>{s.weeklyHours} soat</span></div>
              <div style={{ display:"flex",gap:8 }}>
                <div style={{ flex:1,background:"#F8FAFC",borderRadius:10,padding:"8px 12px",textAlign:"center" }}>
                  <div style={{ fontSize:16,fontWeight:700,color:"#0F172A" }}>{teacherCount}</div>
                  <div style={{ fontSize:10,color:"#94A3B8" }}>O'qituvchi</div>
                </div>
                <div style={{ flex:1,background:"#F8FAFC",borderRadius:10,padding:"8px 12px",textAlign:"center" }}>
                  <div style={{ fontSize:16,fontWeight:700,color:"#0F172A" }}>{lessonsCount}</div>
                  <div style={{ fontSize:10,color:"#94A3B8" }}>Dars/hafta</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  CLASSES
// ═══════════════════════════════════════════════════════════
function ClassesPage({ classes, setClasses, teachers, schedule, toast }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ grade:"5", section:"A", studentCount:"30" });

  const add = () => {
    const name = `${form.grade}-${form.section}`;
    if (classes.find(c=>c.name===name)) return toast(`${name} sinfi allaqachon mavjud!`,"error");
    setClasses(cs=>[...cs,{ id:uid(), name, grade:+form.grade, section:form.section, studentCount:+form.studentCount }]);
    toast(`${name} sinfi qo'shildi ✅`);
    setShowForm(false);
  };

  const byGrade = GRADES.reduce((acc,g)=>{ acc[g]=classes.filter(c=>c.grade===g); return acc; }, {});

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="Sinflar" sub={`${classes.length} ta sinf, ${classes.reduce((a,c)=>a+c.studentCount,0)} o'quvchi`}>
        <Btn icon="plus" onClick={()=>setShowForm(v=>!v)}>Sinf qo'shish</Btn>
      </PageHeader>

      {showForm && (
        <div style={{ background:"#fff",borderRadius:20,padding:24,marginBottom:20,border:"1.5px solid #CCFBF1",animation:"fadeUp .25s ease" }}>
          <div style={{ fontSize:14,fontWeight:700,color:"#0F172A",marginBottom:18 }}>Yangi sinf</div>
          <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:14,marginBottom:18 }}>
            <Select label="Sinf *" value={form.grade} onChange={e=>setForm(f=>({...f,grade:e.target.value}))}>
              {GRADES.map(g=><option key={g}>{g}</option>)}
            </Select>
            <Select label="Sekciya *" value={form.section} onChange={e=>setForm(f=>({...f,section:e.target.value}))}>
              {SECTIONS.map(s=><option key={s}>{s}</option>)}
            </Select>
            <Input label="O'quvchilar soni" type="number" value={form.studentCount} onChange={e=>setForm(f=>({...f,studentCount:e.target.value}))}/>
          </div>
          <div style={{ display:"flex",gap:10 }}>
            <Btn onClick={add}>Saqlash</Btn>
            <Btn variant="ghost" onClick={()=>setShowForm(false)}>Bekor</Btn>
          </div>
        </div>
      )}

      {GRADES.map(g => {
        const gradeClasses = byGrade[g];
        if (gradeClasses.length === 0) return null;
        return (
          <div key={g} style={{ marginBottom:24 }}>
            <div style={{ fontSize:13,fontWeight:700,color:"#94A3B8",marginBottom:10,textTransform:"uppercase",letterSpacing:1 }}>{g}-sinf</div>
            <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12 }}>
              {gradeClasses.map(cls=>{
                const lessonCount = schedule.filter(e=>e.classId===cls.name).length;
                return (
                  <div key={cls.id} style={{ background:"#fff",borderRadius:16,padding:18,boxShadow:"0 1px 8px rgba(0,0,0,.05)",border:"1px solid #F1F5F9",display:"flex",gap:14,alignItems:"center" }}>
                    <div style={{ width:50,height:50,borderRadius:14,background:"linear-gradient(135deg,#0D9488,#0F766E)",display:"flex",alignItems:"center",justifyContent:"center",color:"#fff",fontWeight:800,fontSize:18,flexShrink:0 }}>
                      {cls.name}
                    </div>
                    <div style={{ flex:1,minWidth:0 }}>
                      <div style={{ fontSize:14,fontWeight:700,color:"#0F172A" }}>{cls.name} sinfi</div>
                      <div style={{ fontSize:12,color:"#94A3B8",marginTop:2 }}>{cls.studentCount} o'quvchi</div>

                      <div style={{ fontSize:11,color:"#0D9488",marginTop:3,fontWeight:600 }}>{lessonCount} dars/hafta</div>
                    </div>
                    <button onClick={()=>setClasses(cs=>cs.filter(c=>c.id!==cls.id))} style={{ background:"none",border:"none",cursor:"pointer",color:"#CBD5E1",padding:4 }}><I n="trash" s={15}/></button>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  ROOMS
// ═══════════════════════════════════════════════════════════
function RoomsPage({ rooms, setRooms, schedule, toast }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name:"", capacity:30, type:"oddiy" });

  const add = () => {
    if (!form.name.trim()) return toast("Xona nomini kiriting","error");
    setRooms(rs=>[...rs,{ id:uid(), name:form.name, capacity:+form.capacity, type:form.type }]);
    toast("Xona qo'shildi ✅");
    setForm({ name:"",capacity:30,type:"oddiy" });
    setShowForm(false);
  };

  const roomTypes = { oddiy:"📚 Oddiy sinf",  laboratoriya:"🧪 Laboratoriya", kompyuter:"💻 Kompyuter xona", sport:"⚽ Sporzal" };
  const typeColors = { oddiy:["#EEF2FF","#4338CA"], laboratoriya:["#FDF4FF","#7E22CE"], kompyuter:["#F0F9FF","#0369A1"], sport:["#F0FDF4","#15803D"] };

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="O'quv Xonalari" sub={`${rooms.length} ta xona mavjud`}>
        <Btn icon="plus" onClick={()=>setShowForm(v=>!v)}>Xona qo'shish</Btn>
      </PageHeader>

      {showForm && (
        <div style={{ background:"#fff",borderRadius:20,padding:24,marginBottom:20,border:"1.5px solid #CCFBF1",animation:"fadeUp .25s ease" }}>
          <div style={{ fontSize:14,fontWeight:700,color:"#0F172A",marginBottom:18 }}>Yangi xona</div>
          <div style={{ display:"grid",gridTemplateColumns:"2fr 1fr 1fr",gap:14,marginBottom:18 }}>
            <Input label="Xona nomi *" value={form.name} onChange={e=>setForm(f=>({...f,name:e.target.value}))} placeholder="12-xona, Kimyo lab..."/>
            <Input label="Sig'imi" type="number" value={form.capacity} onChange={e=>setForm(f=>({...f,capacity:e.target.value}))}/>
            <Select label="Turi" value={form.type} onChange={e=>setForm(f=>({...f,type:e.target.value}))}>
              {Object.keys(roomTypes).map(k=><option key={k} value={k}>{roomTypes[k]}</option>)}
            </Select>
          </div>
          <div style={{ display:"flex",gap:10 }}>
            <Btn onClick={add}>Saqlash</Btn>
            <Btn variant="ghost" onClick={()=>setShowForm(false)}>Bekor</Btn>
          </div>
        </div>
      )}

      <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:16 }}>
        {rooms.map(r=>{
          const [bg,tx] = typeColors[r.type] || ["#F1F5F9","#475569"];
          const used = schedule.filter(e=>e.roomId===r.id).length;
          return (
            <div key={r.id} style={{ background:"#fff",borderRadius:20,padding:22,boxShadow:"0 1px 8px rgba(0,0,0,.05)",border:"1px solid #F1F5F9" }}>
              <div style={{ display:"flex",justifyContent:"space-between",marginBottom:14 }}>
                <div style={{ background:bg,color:tx,borderRadius:12,padding:"8px 14px",fontSize:13,fontWeight:600 }}>
                  {roomTypes[r.type]}
                </div>
                <button onClick={()=>setRooms(rs=>rs.filter(x=>x.id!==r.id))} style={{ background:"none",border:"none",cursor:"pointer",color:"#CBD5E1" }}><I n="trash" s={15}/></button>
              </div>
              <div style={{ fontSize:17,fontWeight:700,color:"#0F172A",marginBottom:6 }}>{r.name}</div>
              <div style={{ fontSize:13,color:"#64748B",marginBottom:14 }}>Sig'imi: {r.capacity} o'rin</div>
              <div style={{ display:"flex",gap:10 }}>
                <div style={{ flex:1,background:"#F8FAFC",borderRadius:10,padding:"8px 12px",textAlign:"center" }}>
                  <div style={{ fontSize:16,fontWeight:700,color:used>0?"#0D9488":"#94A3B8" }}>{used}</div>
                  <div style={{ fontSize:10,color:"#94A3B8" }}>Dars/hafta</div>
                </div>
                <div style={{ flex:1,background:"#F8FAFC",borderRadius:10,padding:"8px 12px",textAlign:"center" }}>
                  <div style={{ fontSize:16,fontWeight:700,color:"#0F172A" }}>{Math.round(used/42*100)}%</div>
                  <div style={{ fontSize:10,color:"#94A3B8" }}>Band</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  SCHEDULE
// ═══════════════════════════════════════════════════════════
function SchedulePage({ schedule, teachers, subjects, rooms, classes, toast, setModal }) {
  const [selectedClass, setSelectedClass] = useState("5-A");
  const [viewMode, setViewMode] = useState("class"); // class | teacher
  const [selectedTeacher, setSelectedTeacher] = useState(1);

  const getEntry = (day, period) => {
    if (viewMode==="class") return schedule.find(e=>e.classId===selectedClass && e.day===day && e.period===period);
    return schedule.find(e=>e.teacherId===selectedTeacher && e.day===day && e.period===period);
  };

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="Haftalik Jadval" sub="Darslarni joylashtiring va boshqaring">
        <Btn variant="ghost" icon="print" onClick={()=>window.print()}>Chop etish</Btn>
      </PageHeader>

      {/* Controls */}
      <div style={{ display:"flex",gap:12,marginBottom:20,alignItems:"center",flexWrap:"wrap" }}>
        <div style={{ display:"flex",background:"#F1F5F9",borderRadius:12,padding:4,gap:2 }}>
          {["class","teacher"].map(m=>(
            <button key={m} onClick={()=>setViewMode(m)} style={{ padding:"8px 16px",borderRadius:10,border:"none",cursor:"pointer",fontWeight:600,fontSize:13,background:viewMode===m?"#fff":"transparent",color:viewMode===m?"#0F172A":"#64748B",boxShadow:viewMode===m?"0 1px 4px rgba(0,0,0,.1)":"none",transition:"all .15s" }}>
              {m==="class" ? "Sinf bo'yicha" : "O'qituvchi bo'yicha"}
            </button>
          ))}
        </div>

        {viewMode==="class" ? (
          <div style={{ display:"flex",gap:6,flexWrap:"wrap" }}>
            {["5-A","5-B","6-A","6-B","7-A","7-B","8-A","8-B","9-A"].map(c=>(
              <button key={c} onClick={()=>setSelectedClass(c)} style={{ padding:"7px 14px",borderRadius:10,border:"1.5px solid",fontSize:13,fontWeight:600,background:selectedClass===c?"#0F172A":"#fff",color:selectedClass===c?"#fff":"#64748B",borderColor:selectedClass===c?"#0F172A":"#E2E8F0",cursor:"pointer",transition:"all .15s" }}>{c}</button>
            ))}
          </div>
        ) : (
          <div style={{ display:"flex",gap:6,flexWrap:"wrap" }}>
            {teachers.map(t=>(
              <button key={t.id} onClick={()=>setSelectedTeacher(t.id)} style={{ padding:"7px 14px",borderRadius:10,border:"1.5px solid",fontSize:13,fontWeight:600,background:selectedTeacher===t.id?"#0F172A":"#fff",color:selectedTeacher===t.id?"#fff":"#64748B",borderColor:selectedTeacher===t.id?"#0F172A":"#E2E8F0",cursor:"pointer",transition:"all .15s" }}>{t.name.split(" ")[0]}</button>
            ))}
          </div>
        )}
      </div>

      {/* Grid */}
      <div style={{ background:"#fff",borderRadius:22,overflow:"hidden",boxShadow:"0 2px 20px rgba(0,0,0,.08)",border:"1px solid #F1F5F9" }}>
        {/* Header row */}
        <div style={{ display:"grid",gridTemplateColumns:"100px repeat(6,1fr)",background:"#0F172A" }}>
          <div style={{ padding:"14px 16px",display:"flex",alignItems:"center" }}>
            <span style={{ fontSize:11,color:"rgba(255,255,255,.3)",fontWeight:600,textTransform:"uppercase",letterSpacing:1 }}>Dars</span>
          </div>
          {DAYS.map((d,i)=>(
            <div key={i} style={{ padding:"14px 8px",textAlign:"center",borderLeft:"1px solid rgba(255,255,255,.06)" }}>
              <div style={{ fontSize:12,fontWeight:700,color:"#fff",letterSpacing:.5 }}>{d.slice(0,3).toUpperCase()}</div>
              <div style={{ fontSize:10,color:"rgba(255,255,255,.3)",marginTop:2 }}>{d}</div>
            </div>
          ))}
        </div>

        {PERIODS.map((p,pi)=>(
          <div key={p.num} style={{ display:"grid",gridTemplateColumns:"100px repeat(6,1fr)",borderTop:"1px solid #F1F5F9" }}>
            <div style={{ padding:"12px 16px",background:"#FAFBFC",borderRight:"1px solid #F1F5F9",display:"flex",flexDirection:"column",justifyContent:"center" }}>
              <div style={{ fontSize:13,fontWeight:700,color:"#0F172A" }}>{p.num}-dars</div>
              <div style={{ fontSize:10,color:"#94A3B8",marginTop:2 }}>{p.time}</div>
            </div>
            {DAYS.map((_,di)=>{
              const entry = getEntry(di, p.num);
              const subj = entry ? subjects.find(s=>s.id===entry.subjectId) : null;
              const teacher = entry ? teachers.find(t=>t.id===entry.teacherId) : null;
              const room = entry ? rooms.find(r=>r.id===entry.roomId) : null;
              const [bg,tx,bd] = subj ? sc(subj.name) : [];

              return (
                <div key={di}
                  onClick={()=> entry
                    ? setModal({ type:"viewEntry", entry, subj, teacher, room })
                    : setModal({ type:"addEntry", classId:viewMode==="class"?selectedClass:null, teacherId:viewMode==="teacher"?selectedTeacher:null, day:di, period:p.num })}
                  style={{ minHeight:78,padding:10,borderLeft:"1px solid #F1F5F9",background:entry?bg:"transparent",cursor:"pointer",transition:"background .12s",position:"relative" }}
                  onMouseEnter={e=>{ if(!entry) e.currentTarget.style.background="#F8FAFC"; }}
                  onMouseLeave={e=>{ if(!entry) e.currentTarget.style.background="transparent"; }}>
                  {entry ? (
                    <>
                      <div style={{ fontSize:12,fontWeight:700,color:tx,lineHeight:1.3 }}>{subj?.name}</div>
                      {viewMode==="class" && <div style={{ fontSize:11,color:"#64748B",marginTop:3 }}>{teacher?.name.split(" ")[0]}</div>}
                      {viewMode==="teacher" && <div style={{ fontSize:11,color:"#64748B",marginTop:3 }}>{entry.classId}</div>}
                      {room && <div style={{ fontSize:10,color:"#94A3B8",marginTop:3 }}>🚪 {room.name}</div>}
                    </>
                  ) : (
                    <div style={{ height:"100%",display:"flex",alignItems:"center",justifyContent:"center" }}>
                      <div style={{ width:26,height:26,borderRadius:8,border:"1.5px dashed #E2E8F0",display:"flex",alignItems:"center",justifyContent:"center",color:"#CBD5E1" }}><I n="plus" s={12}/></div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  SWAP (Almashtirish)
// ═══════════════════════════════════════════════════════════
function SwapPage({ teachers, subjects, schedule, setSchedule, toast }) {
  const [absentTeacher, setAbsentTeacher] = useState("");
  const [day, setDay] = useState("0");
  const [results, setResults] = useState([]);

  const findReplacement = () => {
    if (!absentTeacher) return toast("O'qituvchini tanlang","error");
    const tid = +absentTeacher;
    const d = +day;
    const lessons = schedule.filter(e => e.teacherId===tid && e.day===d);
    if (lessons.length===0) return toast("Bu kunda darsi yo'q","error");

    const found = lessons.map(lesson => {
      const subj = subjects.find(s=>s.id===lesson.subjectId);
      const possible = teachers.filter(t =>
        t.id !== tid &&
        t.subjects.includes(lesson.subjectId) &&
        !schedule.find(e => e.teacherId===t.id && e.day===d && e.period===lesson.period)
      );
      return { lesson, subj, possible };
    });
    setResults(found);
  };

  const doSwap = (lessonId, newTeacherId) => {
    setSchedule(s => s.map(e => e.id===lessonId ? {...e, teacherId:newTeacherId} : e));
    const t = teachers.find(x=>x.id===newTeacherId);
    toast(`${t?.name} ga o'tkazildi ✅`);
    setResults(r => r.filter(x => x.lesson.id !== lessonId));
  };

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="O'qituvchi Almashtirish" sub="Kasallik yoki sabab bilan kelmasa, darslarini boshqaga o'tkazish"/>

      <div style={{ background:"#fff",borderRadius:20,padding:24,marginBottom:24,boxShadow:"0 1px 10px rgba(0,0,0,.06)",border:"1px solid #F1F5F9",maxWidth:560 }}>
        <div style={{ fontSize:14,fontWeight:700,color:"#0F172A",marginBottom:18 }}>Qidirish parametrlari</div>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:14,marginBottom:18 }}>
          <Select label="Kelmagan o'qituvchi" value={absentTeacher} onChange={e=>setAbsentTeacher(e.target.value)}>
            <option value="">Tanlang...</option>
            {teachers.map(t=><option key={t.id} value={t.id}>{t.name}</option>)}
          </Select>
          <Select label="Kun" value={day} onChange={e=>setDay(e.target.value)}>
            {DAYS.map((d,i)=><option key={i} value={i}>{d}</option>)}
          </Select>
        </div>
        <Btn icon="swap" onClick={findReplacement}>Almashtiruvchi topish</Btn>
      </div>

      {results.length > 0 && (
        <div style={{ display:"flex",flexDirection:"column",gap:14 }}>
          <div style={{ fontSize:14,fontWeight:700,color:"#0F172A" }}>Topilgan darslar va mumkin bo'lgan almashtiruvchilar:</div>
          {results.map(({lesson, subj, possible}) => (
            <div key={lesson.id} style={{ background:"#fff",borderRadius:18,padding:22,boxShadow:"0 1px 8px rgba(0,0,0,.06)",border:"1px solid #F1F5F9" }}>
              <div style={{ display:"flex",alignItems:"center",gap:12,marginBottom:14 }}>
                <div style={{ background:"#FFF7ED",border:"1px solid #FED7AA",borderRadius:10,padding:"6px 12px",fontSize:13,fontWeight:600,color:"#C2410C" }}>
                  {lesson.period}-dars · {lesson.classId}
                </div>
                {subj && <Tag color={sc(subj.name)[0]} text={sc(subj.name)[1]} border={sc(subj.name)[2]}>{subj.name}</Tag>}
              </div>
              {possible.length === 0 ? (
                <div style={{ color:"#EF4444",fontSize:13,fontWeight:500 }}>⚠ Almashtira oladigan o'qituvchi topilmadi</div>
              ) : (
                <div style={{ display:"flex",gap:10,flexWrap:"wrap" }}>
                  {possible.map(t=>(
                    <button key={t.id} onClick={()=>doSwap(lesson.id, t.id)} style={{ display:"flex",alignItems:"center",gap:8,padding:"10px 16px",background:"#F0FDF4",border:"1.5px solid #86EFAC",borderRadius:12,cursor:"pointer",fontSize:13,fontWeight:600,color:"#15803D" }}>
                      <Avatar name={t.name} id={t.id} size={26}/>
                      {t.name} — O'tkazish
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  CONFLICTS
// ═══════════════════════════════════════════════════════════
function ConflictsPage({ conflicts, schedule, setSchedule, toast }) {
  const typeStyle = {
    class:   { bg:"#FEF2F2", bd:"#FECACA", tx:"#DC2626", icon:"grid"  },
    teacher: { bg:"#FFF7ED", bd:"#FED7AA", tx:"#EA580C", icon:"users" },
    room:    { bg:"#EFF6FF", bd:"#BFDBFE", tx:"#1D4ED8", icon:"door"  },
  };

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="Konfliktlar" sub={conflicts.length > 0 ? `${conflicts.length} ta ziddiyat topildi` : "Hamma yaxshi!"}/>

      {conflicts.length === 0 ? (
        <div style={{ background:"#F0FDF4",border:"1.5px solid #86EFAC",borderRadius:20,padding:40,textAlign:"center" }}>
          <div style={{ fontSize:48,marginBottom:12 }}>✅</div>
          <div style={{ fontSize:18,fontWeight:700,color:"#15803D",marginBottom:6 }}>Jadvalda hech qanday konflikt yo'q!</div>
          <div style={{ color:"#4ADE80",fontSize:14 }}>Barcha darslar to'g'ri joylashtirilgan</div>
        </div>
      ) : (
        <div style={{ display:"flex",flexDirection:"column",gap:12 }}>
          {conflicts.map((c,i) => {
            const s = typeStyle[c.type] || typeStyle.class;
            const labels = { class:"Sinf konflikti", teacher:"O'qituvchi konflikti", room:"Xona konflikti" };
            return (
              <div key={i} style={{ background:s.bg,border:`1.5px solid ${s.bd}`,borderRadius:16,padding:"16px 20px",display:"flex",alignItems:"center",gap:14 }}>
                <div style={{ color:s.tx,flexShrink:0 }}><I n={s.icon} s={20}/></div>
                <div style={{ flex:1 }}>
                  <div style={{ fontSize:12,fontWeight:700,color:s.tx,textTransform:"uppercase",letterSpacing:.5,marginBottom:4 }}>{labels[c.type]}</div>
                  <div style={{ fontSize:14,color:"#0F172A",fontWeight:500 }}>{c.msg}</div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  REPORT
// ═══════════════════════════════════════════════════════════
function ReportPage({ teachers, subjects, rooms, classes, schedule }) {
  const totalLessons = schedule.length;
  const filledSlots = totalLessons;
  const totalSlots = classes.length * 6 * 7;

  const subjectStats = subjects.map(s => ({
    ...s,
    count: schedule.filter(e=>e.subjectId===s.id).length,
    teachers: teachers.filter(t=>t.subjects.includes(s.id)).length,
  })).sort((a,b)=>b.count-a.count);

  const dayStats = DAYS.map((d,i) => ({
    day:d, count: schedule.filter(e=>e.day===i).length
  }));

  const maxDay = Math.max(...dayStats.map(d=>d.count));

  return (
    <div style={{ padding:32 }}>
      <PageHeader title="Hisobot va Statistika" sub="Jadval to'ldirilganlik tahlili"/>

      <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:16,marginBottom:24 }}>
        <StatCard label="Jami dars soatlari" value={totalLessons} sub={`${totalSlots} dan ${filledSlots} ta`} color="#0D9488" icon="calendar"/>
        <StatCard label="To'ldirilganlik" value={`${Math.round(filledSlots/totalSlots*100)}%`} sub="Haftalik jadval" color="#6366F1" icon="chart"/>
        <StatCard label="Jami o'quvchilar" value={classes.reduce((a,c)=>a+c.studentCount,0)} sub={`${classes.length} ta sinfda`} color="#F59E0B" icon="users"/>
      </div>

      <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:20 }}>
        {/* Kunlar bo'yicha */}
        <div style={{ background:"#fff",borderRadius:20,padding:24,boxShadow:"0 1px 10px rgba(0,0,0,.06)",border:"1px solid #F1F5F9" }}>
          <div style={{ fontSize:15,fontWeight:700,color:"#0F172A",marginBottom:20 }}>Kunlar bo'yicha darslar</div>
          {dayStats.map(d=>(
            <div key={d.day} style={{ marginBottom:14 }}>
              <div style={{ display:"flex",justifyContent:"space-between",marginBottom:5 }}>
                <span style={{ fontSize:13,fontWeight:500,color:"#0F172A" }}>{d.day}</span>
                <span style={{ fontSize:13,fontWeight:700,color:"#0D9488" }}>{d.count}</span>
              </div>
              <div style={{ height:8,background:"#F1F5F9",borderRadius:99 }}>
                <div style={{ height:"100%",width:`${d.count/maxDay*100}%`,background:"linear-gradient(90deg,#0D9488,#0F766E)",borderRadius:99,transition:"width .6s ease" }}/>
              </div>
            </div>
          ))}
        </div>

        {/* Fan statistika */}
        <div style={{ background:"#fff",borderRadius:20,padding:24,boxShadow:"0 1px 10px rgba(0,0,0,.06)",border:"1px solid #F1F5F9" }}>
          <div style={{ fontSize:15,fontWeight:700,color:"#0F172A",marginBottom:20 }}>Fanlar bo'yicha</div>
          <div style={{ display:"flex",flexDirection:"column",gap:10 }}>
            {subjectStats.map(s=>{
              const [bg,tx,bd] = sc(s.name);
              return (
                <div key={s.id} style={{ display:"flex",alignItems:"center",gap:12,padding:"10px 12px",background:"#FAFBFC",borderRadius:12 }}>
                  <div style={{ width:36,height:36,borderRadius:10,background:bg,border:`1px solid ${bd}`,display:"flex",alignItems:"center",justifyContent:"center",color:tx,fontWeight:700,fontSize:10 }}>
                    {s.code}
                  </div>
                  <div style={{ flex:1 }}>
                    <div style={{ fontSize:13,fontWeight:600,color:"#0F172A" }}>{s.name}</div>
                    <div style={{ fontSize:11,color:"#94A3B8" }}>{s.teachers} o'qituvchi</div>
                  </div>
                  <div style={{ textAlign:"right" }}>
                    <div style={{ fontSize:16,fontWeight:800,color:tx }}>{s.count}</div>
                    <div style={{ fontSize:10,color:"#94A3B8" }}>dars/hafta</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
//  MODALS
// ═══════════════════════════════════════════════════════════
function AddEntryModal({ classId, teacherId, day, period, teachers, subjects, rooms, schedule, onSave, onClose }) {
  const [f, setF] = useState({ classId: classId||"5-A", teacherId: teacherId||"", subjectId:"", roomId:"" });
  const [err, setErr] = useState("");

  const check = () => {
    if (!f.subjectId || !f.teacherId) return setErr("Fan va o'qituvchini tanlang");
    const tid = +f.teacherId;
    const cid = f.classId;
    if (schedule.find(e=>e.classId===cid && e.day===day && e.period===period))
      return setErr(`❌ ${cid} sinfi bu vaqtda allaqachon band!`);
    if (schedule.find(e=>e.teacherId===tid && e.day===day && e.period===period)) {
      const t = teachers.find(x=>x.id===tid);
      return setErr(`❌ ${t?.name} bu vaqtda boshqa sinfda!`);
    }
    if (f.roomId && schedule.find(e=>e.roomId===+f.roomId && e.day===day && e.period===period)) {
      const r = rooms.find(x=>x.id===+f.roomId);
      return setErr(`❌ ${r?.name} bu vaqtda band!`);
    }
    onSave({ classId:f.classId, teacherId:+f.teacherId, subjectId:+f.subjectId, roomId:f.roomId?+f.roomId:null, day, period });
  };

  return (
    <Modal title={`Dars qo'shish — ${DAYS[day]} ${period}-dars`} onClose={onClose}>
      <div style={{ display:"flex",flexDirection:"column",gap:14 }}>
        {!classId && <Select label="Sinf *" value={f.classId} onChange={e=>setF(x=>({...x,classId:e.target.value}))}>
          {["5-A","5-B","6-A","6-B","7-A","7-B","8-A","8-B","9-A"].map(c=><option key={c}>{c}</option>)}
        </Select>}
        <Select label="Fan *" value={f.subjectId} onChange={e=>setF(x=>({...x,subjectId:e.target.value}))}>
          <option value="">Tanlang...</option>
          {subjects.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}
        </Select>
        {!teacherId && <Select label="O'qituvchi *" value={f.teacherId} onChange={e=>setF(x=>({...x,teacherId:e.target.value}))}>
          <option value="">Tanlang...</option>
          {teachers.map(t=><option key={t.id} value={t.id}>{t.name}</option>)}
        </Select>}
        <Select label="Xona" value={f.roomId} onChange={e=>setF(x=>({...x,roomId:e.target.value}))}>
          <option value="">Tanlang...</option>
          {rooms.map(r=><option key={r.id} value={r.id}>{r.name} ({r.capacity} o'rin)</option>)}
        </Select>
        {err && <div style={{ background:"#FEF2F2",border:"1px solid #FECACA",borderRadius:10,padding:"10px 14px",fontSize:13,color:"#DC2626",fontWeight:500 }}>{err}</div>}
        <div style={{ display:"flex",gap:10,paddingTop:4 }}>
          <Btn style={{ flex:1,justifyContent:"center" }} onClick={check}>✅ Qo'shish</Btn>
          <Btn variant="ghost" onClick={onClose}>Bekor</Btn>
        </div>
      </div>
    </Modal>
  );
}

function ViewEntryModal({ entry, subj, teacher, room, onDelete, onClose }) {
  const [bg,tx,bd] = subj ? sc(subj.name) : ["#F1F5F9","#475569","#E2E8F0"];
  return (
    <Modal title="Dars ma'lumoti" onClose={onClose}>
      <div style={{ display:"flex",flexDirection:"column",gap:14 }}>
        <div style={{ background:bg,border:`1.5px solid ${bd}`,borderRadius:14,padding:18,textAlign:"center" }}>
          <div style={{ fontSize:22,fontWeight:800,color:tx }}>{subj?.name}</div>
          <div style={{ fontSize:14,color:tx,opacity:.7,marginTop:4 }}>{DAYS[entry.day]} · {entry.period}-dars</div>
        </div>
        {[
          ["Sinf", entry.classId],
          ["O'qituvchi", teacher?.name],
          ["Xona", room?.name || "Belgilanmagan"],
        ].map(([label,val])=>(
          <div key={label} style={{ display:"flex",justifyContent:"space-between",padding:"10px 14px",background:"#F8FAFC",borderRadius:10 }}>
            <span style={{ fontSize:13,color:"#64748B" }}>{label}</span>
            <span style={{ fontSize:13,fontWeight:600,color:"#0F172A" }}>{val}</span>
          </div>
        ))}
        <div style={{ display:"flex",gap:10,paddingTop:4 }}>
          <Btn variant="danger" icon="trash" style={{ flex:1,justifyContent:"center" }} onClick={()=>onDelete(entry.id)}>O'chirish</Btn>
          <Btn variant="ghost" onClick={onClose}>Yopish</Btn>
        </div>
      </div>
    </Modal>
  );
}

function AssignSubjectModal({ teacher, subjects, onSave, onClose }) {
  const [selS, setSelS] = useState(teacher.subjects||[]);
  const [selC, setSelC] = useState(teacher.classes||[]);
  const toggle = (arr, set, val) => set(a => a.includes(val) ? a.filter(x=>x!==val) : [...a, val]);

  return (
    <Modal title={`${teacher.name} — Fan va Sinf biriktirish`} width={580} onClose={onClose}>
      <div>
        <div style={{ marginBottom:22 }}>
          <div style={{ fontSize:12,fontWeight:700,color:"#64748B",textTransform:"uppercase",letterSpacing:1,marginBottom:12 }}>Fanlar</div>
          <div style={{ display:"flex",flexWrap:"wrap",gap:8 }}>
            {subjects.map(s=>{
              const active = selS.includes(s.id);
              const [bg,tx,bd] = sc(s.name);
              return (
                <button key={s.id} onClick={()=>toggle(selS,setSelS,s.id)} style={{ padding:"9px 16px",borderRadius:10,border:`1.5px solid ${active?bd:"#E2E8F0"}`,background:active?bg:"#fff",color:active?tx:"#64748B",fontWeight:active?700:400,fontSize:13,cursor:"pointer",display:"flex",alignItems:"center",gap:6,transition:"all .15s" }}>
                  {active && <I n="check" s={12}/>}{s.name}
                </button>
              );
            })}
          </div>
        </div>
        <div style={{ marginBottom:24 }}>
          <div style={{ fontSize:12,fontWeight:700,color:"#64748B",textTransform:"uppercase",letterSpacing:1,marginBottom:12 }}>Sinflar</div>
          <div style={{ display:"grid",gridTemplateColumns:"repeat(5,1fr)",gap:8 }}>
            {["5-A","5-B","6-A","6-B","7-A","7-B","8-A","8-B","9-A","9-B"].map(c=>{
              const active = selC.includes(c);
              return (
                <button key={c} onClick={()=>toggle(selC,setSelC,c)} style={{ padding:"10px 4px",borderRadius:10,border:`1.5px solid ${active?"#0D9488":"#E2E8F0"}`,background:active?"#F0FDFA":"#fff",color:active?"#0F766E":"#64748B",fontWeight:active?700:400,fontSize:13,cursor:"pointer",transition:"all .15s" }}>{c}</button>
              );
            })}
          </div>
          <div style={{ fontSize:12,color:"#94A3B8",marginTop:10 }}>{selC.length} sinf · {selS.length} fan tanlandi</div>
        </div>
        <div style={{ display:"flex",gap:10 }}>
          <Btn style={{ flex:1,justifyContent:"center" }} onClick={()=>onSave(teacher.id,selS,selC)}>✅ Saqlash</Btn>
          <Btn variant="ghost" onClick={onClose}>Bekor</Btn>
        </div>
      </div>
    </Modal>
  );
}

// ═══════════════════════════════════════════════════════════
//  PAGE HEADER
// ═══════════════════════════════════════════════════════════
function PageHeader({ title, sub, children }) {
  return (
    <div style={{ display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:28 }}>
      <div>
        <h1 style={{ fontSize:24,fontWeight:800,color:"#0F172A" }}>{title}</h1>
        {sub && <p style={{ color:"#64748B",marginTop:4,fontSize:14 }}>{sub}</p>}
      </div>
      {children && <div style={{ display:"flex",gap:10,alignItems:"center" }}>{children}</div>}
    </div>
  );
}
