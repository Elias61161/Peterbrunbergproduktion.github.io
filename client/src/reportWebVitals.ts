import { ReportHandler } from 'web-vitals';

// Provide somewhat standardised metrics that are scraped by Google for example
const reportWebVitals = (onPerfEntry?: ReportHandler) => {
    if (onPerfEntry) {
        import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
            getCLS(onPerfEntry);
            getFID(onPerfEntry);
            getFCP(onPerfEntry);
            getLCP(onPerfEntry);
            getTTFB(onPerfEntry);
        });
    }
};

export default reportWebVitals;
