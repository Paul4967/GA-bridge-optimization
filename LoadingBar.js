function blueLoadingBar(totalSteps, interval) {
    const totalWidth = 30; // Width of the loading bar
    let currentStep = 0;

    const intervalId = setInterval(() => {
        currentStep++;
        const progress = currentStep / totalSteps;
        const filledLength = Math.round(progress * totalWidth);
        const bar = '\x1b[44m \x1b[0m'.repeat(filledLength) + ' '.repeat(totalWidth - filledLength); // Blue background
        const percentage = Math.round(progress * 100);

        process.stdout.write(`\r[${bar}] ${percentage}%`); // Overwrites the same line

        if (currentStep >= totalSteps) {
            clearInterval(intervalId);
            process.stdout.write(`\nLoading Complete!\n`);
        }
    }, interval);
}

// Usage example: 50 steps, 100 ms interval
blueLoadingBar(50, 100);
