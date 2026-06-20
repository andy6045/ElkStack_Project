# Power BI Dashboard Setup Guide

## Quick Start (Recommended)

### Option 1: Open the PBIP Project (Power BI Desktop 2023+)
1. Copy the entire `PowerBI_Dashboard_Project` folder to your machine
2. Open Power BI Desktop
3. Go to **File > Open report > Browse this device**
4. Navigate to the folder and open `ProjectManagement.pbip`
5. When prompted, point the data source to `Project_Management_Data_Enhanced.xlsx`
6. Click **Refresh** to load the data
7. **File > Save As** to save as `.pbix`

### Option 2: Import Excel + Apply Measures Manually
1. Open Power BI Desktop
2. **Get Data > Excel Workbook** > select `Project_Management_Data_Enhanced.xlsx`
3. Select the **"Project Data"** sheet > Load
4. Apply the DAX measures from `DAX_Measures.md` below
5. Build visuals following the layout guide

---

## DAX Measures Reference

Copy-paste these into Power BI (Modeling > New Measure):

### P1 - CRITICAL KPIs

```dax
Total Tasks = COUNTROWS(ProjectData)

Completion Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(ProjectData), ProjectData[Status] = "Completed"), 
    COUNTROWS(ProjectData)
)

Average Progress = AVERAGE(ProjectData[Progress])

Tasks Not Started = 
CALCULATE(COUNTROWS(ProjectData), ProjectData[Status] = "Not Started")
```

### P2 - STATUS KPIs

```dax
Tasks Completed = 
CALCULATE(COUNTROWS(ProjectData), ProjectData[Status] = "Completed")

Tasks In Progress = 
CALCULATE(COUNTROWS(ProjectData), ProjectData[Status] = "In Progress")

Tasks Behind Schedule = 
CALCULATE(COUNTROWS(ProjectData), ProjectData[On Track] = "Behind Schedule")

Tasks At Risk = 
CALCULATE(COUNTROWS(ProjectData), ProjectData[On Track] = "At Risk")

Tasks On Track = 
CALCULATE(COUNTROWS(ProjectData), ProjectData[On Track] = "On Track")

Avg Schedule Variance = AVERAGE(ProjectData[Schedule Variance])
```

### P3 - RESOURCE KPIs

```dax
Total Projects = DISTINCTCOUNT(ProjectData[Project Name])

Total Team Members = DISTINCTCOUNT(ProjectData[Assigned To])

Total Effort (Days) = SUM(ProjectData[Days Required])
```

### P4 - DURATION KPIs

```dax
Avg Days Per Task = AVERAGE(ProjectData[Days Required])

Max Task Duration = MAX(ProjectData[Days Required])

Min Task Duration = MIN(ProjectData[Days Required])
```

### Conditional Formatting Helpers

```dax
Completion Rate Color = 
IF(
    [Completion Rate] >= 0.7, "#27AE60", 
    IF([Completion Rate] >= 0.4, "#F39C12", "#E74C3C")
)
```

---

## Dashboard Layout Guide

### Page 1: Executive Overview (Dark Theme: #1B2838)

| Visual | Type | Position | Data |
|--------|------|----------|------|
| Title Bar | Text Box | Top full-width | "PROJECT MANAGEMENT DASHBOARD" |
| Total Tasks | Card | Top row, pos 1 | [Total Tasks] measure |
| Completion Rate | Card | Top row, pos 2 | [Completion Rate] measure |
| Avg Progress | Card | Top row, pos 3 | [Average Progress] measure |
| Not Started | Card | Top row, pos 4 | [Tasks Not Started] measure |
| Projects | Card | Top row, pos 5 | [Total Projects] measure |
| Team Members | Card | Top row, pos 6 | [Total Team Members] measure |
| Status Donut | Donut Chart | Mid-left | Status by Task Count |
| Project Progress | Bar Chart | Mid-right | Avg Progress by Project (sorted desc) |
| Task Details | Table | Bottom | All columns with conditional formatting |

### Page 2: Project Deep Dive (Dark Theme: #1B2838)

| Visual | Type | Position | Data |
|--------|------|----------|------|
| Title Bar | Text Box | Top full-width | "PROJECT DEEP DIVE & TEAM ANALYSIS" |
| Tasks by Status | Clustered Bar | Top-left | Project x Status x Task Count |
| Effort Treemap | Treemap | Top-right | Days by Project (sized by effort) |
| Schedule Health | Donut Chart | Bottom-left | On Track status distribution |
| Team Matrix | Matrix | Bottom-right | Assigned To x Tasks, Progress, Effort |

### Styling Guide
- **Background**: #1B2838 (dark navy)
- **Card backgrounds**: #2C3E50
- **Borders**: #34495E
- **Primary text**: #FFFFFF
- **Secondary text**: #BDC3C7
- **Accent colors**: Blue #3498DB, Green #2ECC71, Red #E74C3C, Orange #F39C12, Purple #9B59B6, Teal #1ABC9C

---

## Files in This Package

| File | Description |
|------|-------------|
| `ProjectManagement.pbip` | Power BI Project file (open in PBI Desktop) |
| `ProjectManagement.Report/report.json` | Report layout with all visuals |
| `ProjectManagement.Report/definition.pbir` | Report definition |
| `ProjectManagement.SemanticModel/model.bim` | Tabular model with 18 DAX measures |
| `ProjectManagement.SemanticModel/definition.pbism` | Semantic model definition |
| `Project_Management_Data_Enhanced.xlsx` | Cleaned Excel with 3 sheets |
| `SETUP_GUIDE.md` | This file |
