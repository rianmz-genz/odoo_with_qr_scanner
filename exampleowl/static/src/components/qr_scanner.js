/** @odoo-module **/

import { registry } from "@web/core/registry";
const { Component, onWillStart, useRef, onMounted, useState } = owl;
import { loadJS } from "@web/core/assets";

export class QrScanner extends Component {
    setup() {
        this.qrReaderRef = useRef("qrReader");
        this.state = useState({ result: "" });

        onWillStart(async () => {
            await loadJS("https://unpkg.com/html5-qrcode");
        });

        onMounted(() => this.initializeQrScanner());
    }

    initializeQrScanner() {
        const onScanSuccess = (decodedText, decodedResult) => {
            this.state.result = `Scanned result: ${decodedText}`;
        };

        const onScanFailure = (error) => {
            console.warn(`QR error: ${error}`);
        };

        const html5QrcodeScanner = new Html5QrcodeScanner(this.qrReaderRef.el.id, {
            fps: 10,
            qrbox: 250,
        });

        html5QrcodeScanner.render(onScanSuccess, onScanFailure);
    }
}

QrScanner.template = "owl.QrScanner";

registry.category("actions").add("owl.qr_scanner", QrScanner);

export default QrScanner;
