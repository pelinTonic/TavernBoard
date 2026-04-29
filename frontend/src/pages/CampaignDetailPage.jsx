import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import api from "../api/axios"
import { useAuth } from "../context/AuthContext"
import NPCModal from "../components/NPCModal"

export default function CampaignDetailPage() {
    const { id } = useParams()
    const navigate = useNavigate()
    const { isDM, user } = useAuth()

    const [campaign, setCampaign] = useState(null)
    const [tab, setTab] = useState("npc")

    const [npcs, setNpcs] = useState([])
    const [members, setMembers] = useState([])

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const [npcModalOpen, setNpcModalOpen] = useState(false)
    const [editingNPC, setEditingNPC] = useState(null)

    useEffect(() => {
        if (!id) return
        fetchCampaign()
        fetchNPCs()
    }, [id])

    async function fetchCampaign() {
        try {
            setLoading(true)
            const res = await api.get(`/campaigns/${id}`)
            setCampaign(res.data)
            setError(null)
        } catch (err) {
            setError("Failed to load campaign")
        } finally {
            setLoading(false)
        }
    }

    async function fetchNPCs() {
        try {
            const res = await api.get(`/campaigns/${id}/npc`)
            setNpcs(res.data)
        } catch (err) {
            console.error("Failed to load NPCs")
        }
    }

    async function deleteCampaign() {
        if (!confirm("Are you sure you want to delete this campaign?")) return

        try {
            await api.delete(`/campaigns/${id}`)
            navigate("/campaigns")
        } catch (err) {
            console.error("Failed to delete campaign")
        }
    }

    function openCreateNPC() {
        setEditingNPC(null)
        setNpcModalOpen(true)
    }

    function openEditNPC(npc) {
        setEditingNPC(npc)
        setNpcModalOpen(true)
    }

    return (
        <div className="bg-tavern min-h-screen">

            {/* NAV */}
            <nav className="navbar">
                <button
                    onClick={() => navigate("/campaigns")}
                    className="btn-ghost"
                >
                    ← Back
                </button>
            </nav>

            <div className="max-w-5xl mx-auto px-6 pt-10">

                {loading && (
                    <p className="text-amber-100/70">Loading...</p>
                )}

                {error && (
                    <p className="text-red-400 mt-4">{error}</p>
                )}

                {campaign && (
                    <>
                        {/* HEADER */}
                        <h1 className="text-amber-200 text-3xl mb-2">
                            {campaign.name}
                        </h1>

                        <p className="text-amber-100/70 mb-4">
                            {campaign.description}
                        </p>

                        {/* DELETE */}
                        {isDM && campaign.dm_id === user?.id && (
                            <button
                                onClick={deleteCampaign}
                                className="btn-ghost text-red-400 mb-6"
                            >
                                Delete Campaign
                            </button>
                        )}

                        {/* TABS */}
                        <div className="flex gap-4 mb-6">
                            <button
                                onClick={() => setTab("npc")}
                                className={`btn-ghost ${tab === "npc" ? "text-amber-300" : ""}`}
                            >
                                NPCs
                            </button>

                            <button
                                onClick={() => setTab("members")}
                                className={`btn-ghost ${tab === "members" ? "text-amber-300" : ""}`}
                            >
                                Members
                            </button>

                            <button
                                onClick={() => setTab("maps")}
                                className={`btn-ghost ${tab === "maps" ? "text-amber-300" : ""}`}
                            >
                                Maps
                            </button>
                        </div>

                        {/* NPC TAB */}
                        {tab === "npc" && (
                            <div>

                                {/* CREATE BUTTON */}
                                {isDM && (
                                    <button
                                        onClick={openCreateNPC}
                                        className="btn-gold mb-4"
                                    >
                                        + New NPC
                                    </button>
                                )}

                                {/* NPC LIST */}
                                {npcs.length === 0 ? (
                                    <p className="text-amber-100/70">
                                        No NPCs yet.
                                    </p>
                                ) : (
                                    <div className="grid grid-cols-2 gap-4">
                                        {npcs.map(npc => (
                                            <div
                                                key={npc.id}
                                                className="card-tavern p-4 cursor-pointer hover:border-amber-600"
                                                onClick={() => openEditNPC(npc)}
                                            >
                                                <div className="flex gap-3 items-center">
                                                    <img
                                                        src={npc.portrait_filename || "/placeholder.png"}
                                                        className="w-12 h-12 object-cover rounded border border-amber-700"
                                                    />

                                                    <div>
                                                        <h3 className="text-amber-200">
                                                            {npc.name}
                                                        </h3>
                                                        <p className="text-amber-100/50 text-xs">
                                                            Click to edit
                                                        </p>
                                                    </div>
                                                </div>

                                                <p className="text-amber-100/70 text-sm mt-2">
                                                    {npc.description}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {/* MEMBERS TAB */}
                        {tab === "members" && (
                            <p className="text-amber-100/70">
                                Members feature coming next.
                            </p>
                        )}

                        {/* MAPS TAB */}
                        {tab === "maps" && (
                            <p className="text-amber-100/70">
                                Maps feature coming next.
                            </p>
                        )}
                    </>
                )}
            </div>

            {/* NPC MODAL */}
            <NPCModal
                open={npcModalOpen}
                onClose={() => setNpcModalOpen(false)}
                campaignId={id}
                existingNPC={editingNPC}
                onSaved={fetchNPCs}
            />
        </div>
    )
}