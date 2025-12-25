function Sidebar({ departmentStats, selectedDepartment, onSelectDepartment, totalCount }) {
    const departments = Object.entries(departmentStats)

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">📚 KM 文件管理</div>

            <div className="sidebar-section">
                <div className="sidebar-section-title">部門分類</div>

                <div
                    className={`sidebar-item ${selectedDepartment === '全部' ? 'active' : ''}`}
                    onClick={() => onSelectDepartment('全部')}
                >
                    <span>📁 全部</span>
                    <span className="sidebar-item-count">{totalCount}</span>
                </div>

                {departments.map(([dept, count]) => (
                    <div
                        key={dept}
                        className={`sidebar-item ${selectedDepartment === dept ? 'active' : ''}`}
                        onClick={() => onSelectDepartment(dept)}
                    >
                        <span>📂 {dept}</span>
                        <span className="sidebar-item-count">{count}</span>
                    </div>
                ))}
            </div>

            <div className="sidebar-section">
                <div className="sidebar-section-title">狀態統計</div>
                <div className="sidebar-item">
                    <span>● 已處理</span>
                    <span className="sidebar-item-count" style={{ background: '#dcfce7', color: '#166534' }}>
                        {totalCount}
                    </span>
                </div>
            </div>
        </aside>
    )
}

export default Sidebar
