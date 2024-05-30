/** @odoo-module */

import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { TopExpenseRenderer } from "./top_expense/top_expense";
import { UserExpenseRenderer } from "./user_expense/user_expense";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart, useRef, onMounted } = owl;

export class OwlSalesDashboard extends Component {
  setup() {}
}

OwlSalesDashboard.template = "owl.OwlSalesDashboard";
OwlSalesDashboard.components = {
  ChartRenderer,
  TopExpenseRenderer,
  UserExpenseRenderer,
};
// OwlSalesDashboard.components = { KpiCard, ChartRenderer };

registry.category("actions").add("owl.sales_dashboard", OwlSalesDashboard);
