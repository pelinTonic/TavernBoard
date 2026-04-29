import { useState } from "react"

function NPCCard({ npc }) {
    const [open, setOpen] = useState(false)

    return (
        <div
            onClick={() => setOpen(o => !o)}
            className="card-tavern cursor-pointer hover:border-amber-700 transition-all duration-300"
        >
            <div className="flex items-center gap-3">

                {/* Portrait */}
                <div className="w-12 h-12 rounded border border-amber-900 overflow-hidden flex-shrink-0">
                    {npc.portrait_filename ? (
                        <img
                            src={`http://localhost:8000/uploads/${npc.portrait_filename}`}
                            alt={npc.name}
                            className="w-full h-full object-cover"
                        />
                    ) : (
                        <div className="w-full h-full bg-amber-950/40 flex items-center justify-center text-xs text-amber-300">
                            ?
                        </div>
                    )}
                </div>

                {/* Name + arrow */}
                <div className="flex-1 flex items-center justify-between">
                    <h3
                        style={{
                            fontFamily: "'Cinzel', serif",
                            color: "#e8d5b0",
                            fontSize: "0.95rem"
                        }}
                    >
                        {npc.name}
                    </h3>

                    <span
                        className={`transition-transform duration-200 text-amber-500 ${
                            open ? "rotate-90" : ""
                        }`}
                    >
                        ▶
                    </span>
                </div>
            </div>

            {/* Expand section */}
            {open && (
                <div className="mt-3 pl-14">
                    <p
                        style={{
                            fontFamily: "'Crimson Text', serif",
                            color: "#8b7355",
                            fontSize: "0.95rem",
                            lineHeight: 1.5
                        }}
                    >
                        {npc.description || "No description available."}
                    </p>
                </div>
            )}
        </div>
    )
}

export default function NPCList({ npcs = [] }) {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
            {npcs.map(npc => (
                <NPCCard key={npc.id} npc={npc} />
            ))}
        </div>
    )
}