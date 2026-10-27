
import streamlit as st
import pandas as pd

from models.vulnerability import get_priority
from services.vulnerability_service import (
    get_all_vulnerabilities,
    add_vulnerability,
    update_vulnerability,
    delete_vulnerability,
)
from algorithms.merge_sort import merge_sort_vulnerabilities
from algorithms.linear_search import linear_search_vulnerability


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="VulnTrack | Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 2. CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }

    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        min-height: 115px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 8px;
        min-height: 42px;
        font-weight: 600;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    .section-caption {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 3. SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🛡️ VulnTrack")
    st.caption("Vulnerability Management System")

    st.divider()

    st.markdown("### Navigation")
    page = st.radio(
        "Choose a section",
        [
            "Overview",
            "Vulnerability Register",
            "Add Vulnerability",
            "Manage Vulnerabilities",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Risk Scoring")
    st.caption(
        "Critical: 65–100\n\n"
        "High: 50–64.99\n\n"
        "Medium: 35–49.99\n\n"
        "Low: 0–34.99"
    )

    st.divider()
    st.caption("Academic DAA + Cybersecurity Project")


# --------------------------------------------------
# 4. APPLICATION HEADER
# --------------------------------------------------

header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("Security Dashboard")
    st.markdown(
        '<p class="section-caption">'
        "Monitor vulnerabilities, assess risk, and prioritize remediation."
        "</p>",
        unsafe_allow_html=True,
    )

with header_col2:
    st.write("")
    st.write("")
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

st.divider()


# --------------------------------------------------
# 5. LOAD AND NORMALIZE DATA
# --------------------------------------------------

@st.cache_data(ttl=0)
def load_vulnerability_records():
    return get_all_vulnerabilities()


try:
    vulnerabilities = load_vulnerability_records()
    vulnerabilities = [dict(item) for item in vulnerabilities]

    # Always derive displayed priority from the current scoring rules.
    for item in vulnerabilities:
        item["priority"] = get_priority(float(item["risk_score"]))

except Exception as error:
    st.error(f"Unable to load vulnerability records: {error}")
    st.stop()


# --------------------------------------------------
# 6. SHARED METRICS
# --------------------------------------------------

total = len(vulnerabilities)

open_count = sum(
    item["status"] == "Open" for item in vulnerabilities
)
progress_count = sum(
    item["status"] == "In Progress" for item in vulnerabilities
)
fixed_count = sum(
    item["status"] == "Fixed" for item in vulnerabilities
)

critical_count = sum(
    item["priority"] == "Critical" for item in vulnerabilities
)
high_count = sum(
    item["priority"] == "High" for item in vulnerabilities
)
medium_count = sum(
    item["priority"] == "Medium" for item in vulnerabilities
)
low_count = sum(
    item["priority"] == "Low" for item in vulnerabilities
)


# --------------------------------------------------
# 7. OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    st.subheader("📊 Security Overview")
    st.caption("A summary of your current vulnerability records.")

    metric_cols = st.columns(4)

    metric_cols[0].metric("Total Findings", total)
    metric_cols[1].metric("Open Issues", open_count)
    metric_cols[2].metric("Critical Findings", critical_count)
    metric_cols[3].metric("Fixed Issues", fixed_count)

    st.divider()

    st.subheader("🚦 Risk Priority Distribution")

    priority_cols = st.columns(4)

    priority_cols[0].metric("🔴 Critical", critical_count)
    priority_cols[1].metric("🟠 High", high_count)
    priority_cols[2].metric("🟡 Medium", medium_count)
    priority_cols[3].metric("🟢 Low", low_count)

    if vulnerabilities:
        chart_col, status_col = st.columns([3, 2])

        with chart_col:
            st.markdown("#### Findings by Priority")

            priority_data = pd.DataFrame({
                "Priority": ["Critical", "High", "Medium", "Low"],
                "Count": [
                    critical_count,
                    high_count,
                    medium_count,
                    low_count,
                ],
            })

            st.bar_chart(
                priority_data,
                x="Priority",
                y="Count",
                color="#12A4D9",
            )

        with status_col:
            st.markdown("#### Remediation Status")

            status_data = pd.DataFrame({
                "Status": ["Open", "In Progress", "Fixed"],
                "Count": [
                    open_count,
                    progress_count,
                    fixed_count,
                ],
            })

            st.bar_chart(
                status_data,
                x="Status",
                y="Count",
                color="#26A69A",
            )

        st.divider()

        st.subheader("🚨 Highest-Risk Findings")

        top_risks = merge_sort_vulnerabilities(
            vulnerabilities,
            descending=True,
        )[:5]

        top_df = pd.DataFrame(top_risks)

        st.dataframe(
            top_df[
                [
                    "vuln_id",
                    "title",
                    "severity",
                    "risk_score",
                    "priority",
                    "status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "risk_score": st.column_config.NumberColumn(
                    "Risk Score",
                    format="%.2f",
                ),
            },
        )

    else:
        st.info(
            "No vulnerability records found. "
            "Open Add Vulnerability to create your first record."
        )

    st.divider()

    st.subheader("📌 Remediation Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        st.write("**Open issues**")
        st.progress(open_count / total if total else 0)
        st.caption(f"{open_count} of {total} total findings")

    with summary_col2:
        st.write("**Fixed issues**")
        st.progress(fixed_count / total if total else 0)
        st.caption(f"{fixed_count} of {total} total findings")


# --------------------------------------------------
# 8. VULNERABILITY REGISTER
# --------------------------------------------------

elif page == "Vulnerability Register":

    st.subheader("🔎 Vulnerability Register")
    st.caption(
        "Search, filter, and sort your findings. "
        "Priority is derived from the current risk score."
    )

    if not vulnerabilities:
        st.info("No records available. Add a vulnerability to get started.")

    else:
        search_col, severity_col, priority_col, status_col = st.columns(4)

        with search_col:
            search_text = st.text_input(
                "Search records",
                placeholder="ID, title, or asset",
            )

        with severity_col:
            severity_filter = st.selectbox(
                "Severity",
                ["All", "Critical", "High", "Medium", "Low"],
            )

        with priority_col:
            priority_filter = st.selectbox(
                "Risk Priority",
                ["All", "Critical", "High", "Medium", "Low"],
            )

        with status_col:
            status_filter = st.selectbox(
                "Status",
                ["All", "Open", "In Progress", "Fixed"],
            )

        filtered_records = vulnerabilities.copy()

        if search_text.strip():
            search = search_text.strip().casefold()

            filtered_records = [
                item for item in filtered_records
                if search in str(item["vuln_id"]).casefold()
                or search in str(item["title"]).casefold()
                or search in str(item["affected_asset"]).casefold()
            ]

        if severity_filter != "All":
            filtered_records = [
                item for item in filtered_records
                if item["severity"] == severity_filter
            ]

        if priority_filter != "All":
            filtered_records = [
                item for item in filtered_records
                if item["priority"] == priority_filter
            ]

        if status_filter != "All":
            filtered_records = [
                item for item in filtered_records
                if item["status"] == status_filter
            ]

        sort_col, count_col = st.columns([2, 4])

        with sort_col:
            sort_order = st.selectbox(
                "Sort by risk score",
                ["Highest Risk First", "Lowest Risk First"],
            )

        filtered_records = merge_sort_vulnerabilities(
            filtered_records,
            descending=(sort_order == "Highest Risk First"),
        )

        with count_col:
            st.write("")
            st.caption(
                f"Showing {len(filtered_records)} of {total} vulnerabilities"
            )

        if filtered_records:
            filtered_df = pd.DataFrame(filtered_records)

            display_columns = [
                "vuln_id",
                "title",
                "affected_asset",
                "severity",
                "risk_score",
                "priority",
                "remediation_hours",
                "status",
            ]

            st.dataframe(
                filtered_df[display_columns],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "risk_score": st.column_config.NumberColumn(
                        "Risk Score",
                        format="%.2f",
                    ),
                    "remediation_hours": st.column_config.NumberColumn(
                        "Remediation Hours",
                        format="%.1f",
                    ),
                },
            )

            st.download_button(
                "⬇️ Export Filtered Records (CSV)",
                data=filtered_df[display_columns].to_csv(index=False),
                file_name="vulntrack_vulnerabilities.csv",
                mime="text/csv",
            )

        else:
            st.warning("No records match your selected search and filters.")

        st.divider()

        st.subheader("🔍 Find Vulnerability by ID")

        search_id = st.text_input(
            "Enter an exact vulnerability ID",
            placeholder="VUL-001",
            key="linear_search_id",
        )

        if search_id.strip():
            result = linear_search_vulnerability(
                vulnerabilities,
                search_id.strip(),
            )

            if result is not None:
                # Use the same priority calculation for search results.
                result = dict(result)
                result["priority"] = get_priority(
                    float(result["risk_score"])
                )

                st.success("Vulnerability found!")

                result_cols = st.columns(3)
                result_cols[0].metric("Risk Score", result["risk_score"])
                result_cols[1].metric("Priority", result["priority"])
                result_cols[2].metric("Status", result["status"])

                st.write(f"**ID:** {result['vuln_id']}")
                st.write(f"**Title:** {result['title']}")
                st.write(f"**Affected Asset:** {result['affected_asset']}")
                st.write(f"**Severity:** {result['severity']}")

            else:
                st.warning("No vulnerability found with that ID.")

# --------------------------------------------------
# 9. ADD VULNERABILITY
# --------------------------------------------------

elif page == "Add Vulnerability":

    st.subheader("➕ Add Vulnerability")
    st.caption(
        "Enter the vulnerability details and estimate its risk factors."
    )

    with st.form("add_vulnerability_form", clear_on_submit=True):

        st.markdown("#### 1. Vulnerability Details")

        id_col, title_col = st.columns(2)

        with id_col:
            vuln_id = st.text_input(
                "Vulnerability ID",
                placeholder="VUL-001",
            )

        with title_col:
            title = st.text_input(
                "Vulnerability Title",
                placeholder="SQL Injection in Login Form",
            )

        affected_asset = st.text_input(
            "Affected Asset",
            placeholder="Web Application",
        )

        st.divider()
        st.markdown("#### 2. Risk Assessment")

        severity_col, criticality_col = st.columns(2)

        with severity_col:
            severity = st.selectbox(
                "Severity",
                ["Critical", "High", "Medium", "Low"],
            )

            exploitability = st.slider(
                "Exploitability",
                min_value=1,
                max_value=10,
                value=7,
                help="Higher values indicate easier exploitation.",
            )

            impact = st.slider(
                "Impact",
                min_value=1,
                max_value=10,
                value=7,
                help="Higher values indicate greater potential impact.",
            )

        with criticality_col:
            asset_criticality = st.slider(
                "Asset Criticality",
                min_value=1,
                max_value=5,
                value=3,
                help="Rate the importance of the affected asset.",
            )

            remediation_hours = st.number_input(
                "Estimated Remediation Hours",
                min_value=0.5,
                max_value=10000.0,
                value=3.0,
                step=0.5,
            )

            status = st.selectbox(
                "Remediation Status",
                ["Open", "In Progress", "Fixed"],
            )

        submitted = st.form_submit_button(
            "Save Vulnerability",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not vuln_id.strip() or not title.strip() or not affected_asset.strip():
                st.error(
                    "Please fill in the vulnerability ID, title, and affected asset."
                )

            elif any(
                item["vuln_id"].casefold() == vuln_id.strip().casefold()
                for item in vulnerabilities
            ):
                st.error("That vulnerability ID already exists.")

            else:
                try:
                    add_vulnerability(
                        vuln_id=vuln_id.strip(),
                        title=title.strip(),
                        affected_asset=affected_asset.strip(),
                        severity=severity,
                        exploitability=exploitability,
                        impact=impact,
                        asset_criticality=asset_criticality,
                        remediation_hours=remediation_hours,
                        status=status,
                    )

                    st.success(
                        f"Vulnerability {vuln_id.strip()} added successfully!"
                    )
                    st.rerun()

                except ValueError as error:
                    st.error(str(error))

                except Exception as error:
                    st.error(f"Unable to save the vulnerability: {error}")


# --------------------------------------------------
# 10. MANAGE VULNERABILITIES
# --------------------------------------------------

elif page == "Manage Vulnerabilities":

    st.subheader("🛠️ Manage Vulnerabilities")
    st.caption("Update remediation details or delete a record.")

    if not vulnerabilities:
        st.info("No vulnerability records are available to manage.")

    else:
        selected_id = st.selectbox(
            "Select a vulnerability",
            options=[item["vuln_id"] for item in vulnerabilities],
            format_func=lambda value: next(
                (
                    f"{item['vuln_id']} — {item['title']}"
                    for item in vulnerabilities
                    if item["vuln_id"] == value
                ),
                value,
            ),
        )

        selected_record = next(
            item for item in vulnerabilities
            if item["vuln_id"] == selected_id
        )

        info_col1, info_col2, info_col3 = st.columns(3)

        info_col1.metric(
            "Risk Score",
            f"{float(selected_record['risk_score']):.2f}",
        )
        info_col2.metric(
            "Priority",
            selected_record["priority"],
        )
        info_col3.metric(
            "Status",
            selected_record["status"],
        )

        st.write(f"**Affected Asset:** {selected_record['affected_asset']}")

        update_tab, delete_tab = st.tabs(
            ["✏️ Update Record", "🗑️ Delete Record"]
        )

        with update_tab:
            with st.form("update_vulnerability_form"):

                st.markdown("#### Update vulnerability information")

                new_status = st.selectbox(
                    "Remediation Status",
                    ["Open", "In Progress", "Fixed"],
                    index=["Open", "In Progress", "Fixed"].index(
                        selected_record["status"]
                    ),
                )

                new_severity = st.selectbox(
                    "Severity",
                    ["Critical", "High", "Medium", "Low"],
                    index=["Critical", "High", "Medium", "Low"].index(
                        selected_record["severity"]
                    ),
                )

                new_exploitability = st.slider(
                    "Exploitability",
                    min_value=1,
                    max_value=10,
                    value=int(selected_record["exploitability"]),
                )

                new_impact = st.slider(
                    "Impact",
                    min_value=1,
                    max_value=10,
                    value=int(selected_record["impact"]),
                )

                new_criticality = st.slider(
                    "Asset Criticality",
                    min_value=1,
                    max_value=5,
                    value=int(selected_record["asset_criticality"]),
                )

                new_hours = st.number_input(
                    "Remediation Hours",
                    min_value=0.5,
                    max_value=10000.0,
                    value=float(selected_record["remediation_hours"]),
                    step=0.5,
                )

                update_clicked = st.form_submit_button(
                    "Save Changes",
                    type="primary",
                    use_container_width=True,
                )

                if update_clicked:
                    try:
                        updated = update_vulnerability(
                            selected_id,
                            status=new_status,
                            severity=new_severity,
                            exploitability=new_exploitability,
                            impact=new_impact,
                            asset_criticality=new_criticality,
                            remediation_hours=new_hours,
                        )

                        if updated:
                            st.success("Vulnerability updated successfully.")
                            st.rerun()
                        else:
                            st.error("The selected vulnerability was not found.")

                    except (ValueError, TypeError) as error:
                        st.error(str(error))

                    except Exception as error:
                        st.error(f"Update failed: {error}")

        with delete_tab:
            st.warning(
                f"You are about to permanently delete {selected_id}. "
                "This action cannot be undone."
            )

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this vulnerability.",
                key=f"confirm_delete_{selected_id}",
            )

            if st.button(
                "Delete Vulnerability",
                type="primary",
                disabled=not confirm_delete,
                use_container_width=True,
            ):
                try:
                    deleted = delete_vulnerability(selected_id)

                    if deleted:
                        st.success("Vulnerability deleted successfully.")
                        st.rerun()
                    else:
                        st.error("The selected vulnerability was not found.")

                except Exception as error:
                    st.error(f"Deletion failed: {error}")


# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------

st.divider()

footer_col1, footer_col2 = st.columns(2)

with footer_col1:
    st.caption("🛡️ VulnTrack | Academic DAA + Cybersecurity Project")

with footer_col2:
    st.caption(
        "Risk scores and priorities are for vulnerability triage "
        "and should be validated before operational use."
    )
