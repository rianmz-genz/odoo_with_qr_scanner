/** @odoo-module */

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart, useRef, onMounted, useState } = owl;

export class ChartRenderer extends Component {
  setup() {
    this.chartRef = useRef("chart");
    this.chartData = [];

    var apiUrl = "103.127.137.215:3000/pettycash/list";

    onWillStart(async () => {
      await loadJS(
        "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"
      );

      try {
        const response = await fetch(apiUrl);
        // console.log(response);
        if (!response.ok) {
          console.log("ERROR NYET");
          return;
        }

        const data = await response.json();
        console.log("INI BG", data);
        // this.chartData.push(data.data.map((item) => item.kredit_sum));

        for (let i = 1; i <= 12; i++) {
          const month = String(i).padStart(2, "0");

          const monthData = data.data.find((item) =>
            item.tanggal_transaksi.endsWith(`-${month}`)
          );

          if (monthData) {
            this.chartData.push(monthData.debit_sum);
          } else {
            this.chartData.push(0);
          }
        }
      } catch (error) {
        console.error(error);
      }
    });

    async function getValue() {
      // Get the input element
      const year = document.getElementById("year");

      // Get the value from the input element
      const yearValue = year.value;

      // Return the yearValue
      return yearValue;
    }

    onMounted(() => this.renderChart());
  }

  chartData() {}

  renderChart() {
    console.log("IYA BG", this.yearValue);
    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    new Chart(this.chartRef.el, {
      type: this.props.type,
      data: {
        labels: months,
        datasets: [
          // {
          //   label: "Saldo Kas Kecil",
          //   data: [300, 50, 100, 70],
          //   hoverOffset: 4,
          // },
          {
            label: "Pengeluaran",
            data: this.chartData,
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
          // title: {
          //   display: true,
          //   text: this.props.title,
          //   position: "bottom",
          // },
        },
      },
    });
  }
}

ChartRenderer.template = "owl.ChartRenderer";
