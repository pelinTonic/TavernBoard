import { useState, useEffect } from "react"
import api from "../api/axios"

export default function NPCModal({
    open,
    onClose,
    campaignId,
    onSaved,
    existingNPC = null
}) {
    const isEdit = !!existingNPC

    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [file, setFile] = useState(null)
    const [preview, setPreview] = useState(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        if (existingNPC) {
            setName(existingNPC.name || "")
            setDescription(existingNPC.description || "")
            setPreview(existingNPC.portrait_filename || null)
        } else {
            setName("")
            setDescription("")
            setPreview(null)
            setFile(null)
        }
    }, [existingNPC, open])

    if (!open) return null

    function handleFileChange(e) {
        const f = e.target.files[0]
        setFile(f)
        if (f) setPreview(URL.createObjectURL(f))
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setLoading(true)

        try {
            const formData = new FormData()
            formData.append("name", name)
            formData.append("description", description)

            if (file) {
                formData.append("file", file)
            }

            if (isEdit) {
                await api.put(
                    `/campaigns/${campaignId}/npc/${existingNPC.id}`,
                    formData,
                    { headers: { "Content-Type": "multipart/form-data" } }
                )
            } else {
                await api.post(
                    `/campaigns/${campaignId}/npc`,
                    formData,
                    { headers: { "Content-Type": "multipart/form-data" } }
                )
            }

            onSaved()
            onClose()
        } catch (err) {
            console.error("NPC save failed:", err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
            <div className="card-tavern w-[420px] p-5 animate-fade-up">

                <h2 className="text-amber-200 text-lg mb-4 text-center">
                    {isEdit ? "Edit NPC" : "Create NPC"}
                </h2>

                <form onSubmit={handleSubmit} className="flex flex-col gap-3">

                    <input
                        className="input-tavern"
                        placeholder="NPC name"
                        value={name}
                        onChange={e => setName(e.target.value)}
                    />

                    <textarea
                        className="input-tavern"
                        placeholder="Description"
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        style={{ minHeight: "90px", resize: "none" }}
                    />

                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileChange}
                    />

                    {preview && (
                        <img
                            src={preview}
                            className="w-20 h-20 object-cover rounded border border-amber-700"
                        />
                    )}

                    <div className="flex justify-end gap-2 mt-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn-ghost"
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            className="btn-gold"
                            disabled={loading}
                        >
                            {loading ? "Saving..." : "Save NPC"}
                        </button>
                    </div>

                </form>
            </div>
        </div>
    )
}