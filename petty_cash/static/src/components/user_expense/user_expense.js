/** @odoo-module */

const { Component, onWillStart, useRef, onMounted } = owl;

export class UserExpenseRenderer extends Component {
  setup() {
    this.userExpenseRef = useRef("user-expense");
    this.userExpenseData = {};

    var apiUrl = "103.127.137.215:3000/pettycash/list/top-user-expense";

    onWillStart(async () => {
      try {
        const res = await fetch(apiUrl);
        if (!res.ok) {
          // console.log("ERROR NYET");
          return;
        }

        // console.log("STATUS", res.status);

        const data = await res.json();
        // console.log("API Data:", data);

        // Assign the data directly to userExpenseData
        if (data.data != null) {
          this.userExpenseData = Object.values(data.data)
            .filter((item) => item.debit_sum !== 0) // Filter out elements with debit_sum === 0
            .sort((a, b) => b.debit_sum - a.debit_sum);
        }

        console.log(this.userExpenseData);
      } catch (error) {
        console.error(error);
      }
    });

    // onMounted(() => this.renderTopExpense());
  }

  // renderTopExpense() {
  //   // You can customize the rendering based on your requirements
  //   console.log("Rendering Top 10 Expenses", this.userExpenseData);
  //   if (this.userExpenseData) {
  //     //   this.userExpenseRef.el.innerHTML = this.env.qweb.render(
  //     //     "owl.UserExpenseRenderer",
  //     //     {
  //     //       userExpenseData: this.userExpenseData,
  //     //     }
  //     //   );
  //   }
  // }
}

UserExpenseRenderer.template = "owl.UserExpenseRenderer";
