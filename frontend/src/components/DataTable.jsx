import { useState } from 'react'

function DataTable({ documents, onEdit }) {
    const [sortField, setSortField] = useState('doc_id')
    const [sortOrder, setSortOrder] = useState('asc')

    const handleSort = (field) => {
        if (sortField === field) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
        } else {
            setSortField(field)
            setSortOrder('asc')
        }
    }

    const sortedDocuments = [...documents].sort((a, b) => {
        const aVal = a[sortField] || ''
        const bVal = b[sortField] || ''
        const compare = aVal.toString().localeCompare(bVal.toString())
        return sortOrder === 'asc' ? compare : -compare
    })

    const getStatusBadge = (doc) => {
        const version = doc.versions?.[doc.versions.length - 1]
        if (version?.ai_processed) {
            return <span className="status-badge processed">✅ 已處理</span>
        }
        if (doc.status === 'draft') {
            return <span className="status-badge draft">📝 草稿</span>
        }
        return <span className="status-badge pending">⏳ 待處理</span>
    }

    const getChunkCount = (doc) => {
        const version = doc.versions?.[doc.versions.length - 1]
        return version?.chunk_count || 0
    }

    return (
        <table className="data-table">
            <thead>
                <tr>
                    <th onClick={() => handleSort('doc_id')}>
                        文件編號 {sortField === 'doc_id' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th onClick={() => handleSort('title')}>
                        文件名稱 {sortField === 'title' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th onClick={() => handleSort('department')}>
                        部門 {sortField === 'department' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th onClick={() => handleSort('category')}>
                        分類 {sortField === 'category' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </th>
                    <th>版本</th>
                    <th>Chunks</th>
                    <th>狀態</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {sortedDocuments.map((doc) => (
                    <tr key={doc.doc_id}>
                        <td><strong>{doc.doc_id}</strong></td>
                        <td>{doc.title}</td>
                        <td>{doc.department}</td>
                        <td>{doc.category}</td>
                        <td>v{doc.current_version}</td>
                        <td>{getChunkCount(doc)}</td>
                        <td>{getStatusBadge(doc)}</td>
                        <td>
                            <button className="action-btn" title="查看">👁️</button>
                            <button className="action-btn" title="編輯" onClick={() => onEdit?.(doc)}>✏️</button>
                            <button className="action-btn" title="AI 分析">✨</button>
                        </td>
                    </tr>
                ))}
                {sortedDocuments.length === 0 && (
                    <tr>
                        <td colSpan="8" style={{ textAlign: 'center', padding: '32px', color: '#6b7280' }}>
                            暫無文件資料
                        </td>
                    </tr>
                )}
            </tbody>
        </table>
    )
}

export default DataTable
