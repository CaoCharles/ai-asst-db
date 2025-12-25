import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Library from './pages/Library'
import './index.css'

function App() {
  const [documents, setDocuments] = useState([])
  const [selectedDepartment, setSelectedDepartment] = useState('全部')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 載入文件清單
    fetch('/data/manifest.json')
      .then(res => res.json())
      .then(data => {
        setDocuments(data.documents || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('載入失敗:', err)
        setLoading(false)
      })
  }, [])

  // 計算部門統計
  const departmentStats = documents.reduce((acc, doc) => {
    const dept = doc.department || '未分類'
    acc[dept] = (acc[dept] || 0) + 1
    return acc
  }, {})

  // 篩選文件
  const filteredDocuments = selectedDepartment === '全部'
    ? documents
    : documents.filter(doc => doc.department === selectedDepartment)

  return (
    <div className="app-layout">
      <Sidebar
        departmentStats={departmentStats}
        selectedDepartment={selectedDepartment}
        onSelectDepartment={setSelectedDepartment}
        totalCount={documents.length}
      />
      <main className="main-content">
        <Library
          documents={filteredDocuments}
          loading={loading}
          onDocumentsChange={setDocuments}
        />
      </main>
    </div>
  )
}

export default App
