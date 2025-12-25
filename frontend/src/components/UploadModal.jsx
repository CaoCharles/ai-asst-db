import { useState, useRef } from 'react'

function UploadModal({ isOpen, onClose, onUpload }) {
    const [formData, setFormData] = useState({
        doc_id: '',
        title: '',
        department: '人資部',
        category: '辦法',
        keywords: ''
    })
    const [dragOver, setDragOver] = useState(false)
    const [selectedFile, setSelectedFile] = useState(null)
    const fileInputRef = useRef(null)

    if (!isOpen) return null

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setDragOver(false)
        const file = e.dataTransfer.files[0]
        if (file) {
            setSelectedFile(file)
            // 自動填入文件名稱
            if (!formData.title) {
                setFormData({ ...formData, title: file.name.replace(/\.[^/.]+$/, '') })
            }
        }
    }

    const handleFileSelect = (e) => {
        const file = e.target.files[0]
        if (file) {
            setSelectedFile(file)
            if (!formData.title) {
                setFormData({ ...formData, title: file.name.replace(/\.[^/.]+$/, '') })
            }
        }
    }

    const handleSubmit = () => {
        if (!formData.doc_id || !formData.title) {
            alert('請填寫文件編號和名稱')
            return
        }

        // 建立新文件資料
        const newDoc = {
            doc_id: formData.doc_id,
            title: formData.title,
            department: formData.department,
            category: formData.category,
            sub_category: formData.category,
            current_version: 1,
            status: 'active',
            versions: [
                {
                    version: 1,
                    file_name: selectedFile?.name || `${formData.doc_id}.json`,
                    raw_path: `raw/${selectedFile?.name || formData.doc_id + '.json'}`,
                    processed_path: `processed/${formData.doc_id}_chunks.json`,
                    uploaded_at: new Date().toISOString().split('T')[0],
                    uploaded_by: 'admin',
                    description: '初版',
                    ai_processed: false,
                    chunk_count: 0
                }
            ],
            metadata: {
                keywords: formData.keywords.split(',').map(k => k.trim()).filter(Boolean)
            }
        }

        onUpload(newDoc)
        onClose()

        // 重置表單
        setFormData({
            doc_id: '',
            title: '',
            department: '人資部',
            category: '辦法',
            keywords: ''
        })
        setSelectedFile(null)
    }

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2 className="modal-title">上傳新文件</h2>
                    <button className="modal-close" onClick={onClose}>✕</button>
                </div>

                <div className="modal-body">
                    <div
                        className={`upload-zone ${dragOver ? 'dragover' : ''}`}
                        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
                        onDragLeave={() => setDragOver(false)}
                        onDrop={handleDrop}
                        onClick={() => fileInputRef.current?.click()}
                    >
                        <div className="upload-icon">📄</div>
                        {selectedFile ? (
                            <div><strong>{selectedFile.name}</strong></div>
                        ) : (
                            <>
                                <div className="upload-text">拖曳檔案至此</div>
                                <div className="upload-text">或 點擊選擇檔案</div>
                            </>
                        )}
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleFileSelect}
                            style={{ display: 'none' }}
                            accept=".json,.pdf,.docx,.txt"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">文件編號 *</label>
                        <input
                            type="text"
                            className="form-input"
                            name="doc_id"
                            value={formData.doc_id}
                            onChange={handleChange}
                            placeholder="例如: HR-002"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">文件名稱 *</label>
                        <input
                            type="text"
                            className="form-input"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            placeholder="例如: 員工考勤管理辦法"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">部門</label>
                        <select
                            className="form-select"
                            name="department"
                            value={formData.department}
                            onChange={handleChange}
                        >
                            <option value="人資部">人資部</option>
                            <option value="法遵部">法遵部</option>
                            <option value="業務部">業務部</option>
                            <option value="IT部">IT部</option>
                            <option value="財務部">財務部</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label">分類</label>
                        <select
                            className="form-select"
                            name="category"
                            value={formData.category}
                            onChange={handleChange}
                        >
                            <option value="法規">法規</option>
                            <option value="辦法">辦法</option>
                            <option value="SOP">SOP</option>
                            <option value="訓練教材">訓練教材</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label">關鍵字（以逗號分隔）</label>
                        <input
                            type="text"
                            className="form-input"
                            name="keywords"
                            value={formData.keywords}
                            onChange={handleChange}
                            placeholder="例如: 考勤, 打卡, 出勤"
                        />
                    </div>
                </div>

                <div className="modal-footer">
                    <button className="btn" onClick={onClose}>取消</button>
                    <button className="btn btn-primary" onClick={handleSubmit}>
                        上傳
                    </button>
                </div>
            </div>
        </div>
    )
}

export default UploadModal
