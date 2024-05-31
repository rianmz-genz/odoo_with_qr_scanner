/** @odoo-module */

import { registry } from "@web/core/registry";
const { Component, onWillStart, useRef, onMounted } = owl;

export class TopExpenseRenderer extends Component {
  setup() {
    this.topExpenseRef = useRef("top-expense");
    this.topExpenseData = {};

    var apiUrl = "pettycash/list/top-expense";

    onWillStart(async () => {
      try {
        const res = await fetch(apiUrl);
        if (!res.ok) {
          // console.log("ERROR NYET");
          return;
        }

        // console.log("STATUS", res.status);

        const data = await res.json();
        console.log("API Data:", data);

        // Assign the data directly to topExpenseData
        if (data.data != null) {
          this.topExpenseData = Object.values(data.data)
            .filter((item) => item.debit_sum !== 0) // Filter out elements with debit_sum === 0
            .sort((a, b) => b.debit_sum - a.debit_sum);
        }

        // console.log(this.topExpenseData);
      } catch (error) {
        console.error(error);
      }
    });

    // onMounted(() => this.renderTopExpense());
  }

  // renderTopExpense() {
  //   // You can customize the rendering based on your requirements
  //   console.log("Rendering Top 10 Expenses", this.topExpenseData);
  //   if (this.topExpenseData) {
  //     //   this.topExpenseRef.el.innerHTML = this.env.qweb.render(
  //     //     "owl.TopExpenseRenderer",
  //     //     {
  //     //       topExpenseData: this.topExpenseData,
  //     //     }
  //     //   );
  //   }
  // }
}

TopExpenseRenderer.template = "owl.TopExpenseRenderer";
