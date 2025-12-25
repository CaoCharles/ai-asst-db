import { useState } from 'react'
import DataTable from '../components/DataTable'
import UploadModal from '../components/UploadModal'

function Library({ documents, loading, onDocumentsChange }) {
    const [searchTerm, setSearchTerm] = useState('')
    const [statusFilter, setStatusFilter] = useState('全部')
    const [isUploadOpen, setIsUploadOpen] = useState(false)

    // 搜尋過濾
    const filteredDocuments = documents.filter(doc => {
        const matchSearch = !searchTerm ||
            doc.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            doc.doc_id?.toLowerCase().includes(searchTerm.toLowerCase())

        const matchStatus = statusFilter === '全部' ||
            (statusFilter === '已處理' && doc.versions?.[doc.versions.length - 1]?.ai_processed) ||
            (statusFilter === '待處理' && !doc.versions?.[doc.versions.length - 1]?.ai_processed)

        return matchSearch && matchStatus
    })

    const handleUpload = (newDoc) => {
        onDocumentsChange([...documents, newDoc])
    }

    const handleExport = () => {
        // 匯出為 JSON（模擬 Excel）
        const dataStr = JSON.stringify(documents, null, 2)
        const blob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'documents.json'
        a.click()
    }

    if (loading) {
        return <div style={{ padding: '32px', textAlign: 'center' }}>載入中...</div>
    }

    return (
        <>
            <div className="page-header">
                <h1 className="page-title">📚 文件清單</h1>
                <div style={{ display: 'flex', gap: '8px' }}>
                    <button className="btn" onClick={handleExport}>
                        ⬇️ 匯出
                    </button>
                    <button className="btn btn-primary" onClick={() => setIsUploadOpen(true)}>
                        ➕ 上傳文件
                    </button>
                </div>
            </div>

            <div className="search-bar">
                <input
                    type="text"
                    className="search-input"
                    placeholder="🔍 搜尋文件編號或名稱..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <select
                    className="filter-select"
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                >
                    <option value="全部">狀態: 全部</option>
                    <option value="已處理">已處理</option>
                    <option value="待處理">待處理</option>
                </select>
            </div>

            <DataTable documents={filteredDocuments} />

            <div className="pagination">
                <div className="pagination-info">
                    顯示 1-{filteredDocuments.length} / 共 {filteredDocuments.length} 筆
                </div>
            </div>

            <UploadModal
                isOpen={isUploadOpen}
                onClose={() => setIsUploadOpen(false)}
                onUpload={handleUpload}
            />
        </>
    )
}

export default Library
