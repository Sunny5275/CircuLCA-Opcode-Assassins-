/* ==========================================
   LCA Metallurgy App - Enhanced JavaScript
   Modern User Interactions & Animations
   ========================================== */

// Application State Management
class LCAApp {
    constructor() {
        this.currentResults = null;
        this.HISTORY_KEY = 'lca_calculation_history';
        this.MAX_HISTORY_ITEMS = 20;
        this.isLoading = false;
        
        // Initialize the application
        this.init();
    }

    // Initialize application
    init() {
        this.bindEvents();
        this.loadHistoryFromStorage();
        this.initFormValidation();
        this.initKeyboardShortcuts();
        this.initTooltips();
        this.showWelcomeAnimation();
    }

    // Bind event listeners
    bindEvents() {
        const form = document.getElementById('lcaForm');
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }

        // Form field validation on blur
        const formFields = document.querySelectorAll('.form-control');
        formFields.forEach(field => {
            field.addEventListener('blur', this.validateField.bind(this));
            field.addEventListener('input', this.clearFieldErrors.bind(this));
        });

        // Auto-save form data
        formFields.forEach(field => {
            field.addEventListener('change', this.autoSaveFormData.bind(this));
        });

        // Load saved form data
        this.loadSavedFormData();
    }

    // Initialize keyboard shortcuts
    initKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+N or Cmd+N for new LCA calculation
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                this.startNewLCA();
            }
            
            // Escape key to clear form
            if (e.key === 'Escape') {
                this.startNewLCA();
            }

            // Ctrl+S to save current state (prevent default browser save)
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                this.autoSaveFormData();
                this.showNotification('Form data saved locally', 'info');
            }
        });
    }

    // Initialize tooltips for help text
    initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            this.createTooltip(element);
        });
    }

    // Create tooltip element
    createTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.getAttribute('data-tooltip');
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(5, 5, 5, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            pointer-events: none;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            max-width: 200px;
            line-height: 1.4;
        `;

        element.addEventListener('mouseenter', () => {
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(0)';
        });

        element.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (tooltip.parentNode) {
                    tooltip.parentNode.removeChild(tooltip);
                }
            }, 300);
        });
    }

    // Show welcome animation
    showWelcomeAnimation() {
        const container = document.querySelector('.container');
        const historyPanel = document.querySelector('.history-panel');
        
        if (container && historyPanel) {
            container.style.opacity = '0';
            container.style.transform = 'translateY(30px)';
            historyPanel.style.opacity = '0';
            historyPanel.style.transform = 'translateX(30px)';

            setTimeout(() => {
                container.style.transition = 'all 0.8s ease-out';
                container.style.opacity = '1';
                container.style.transform = 'translateY(0)';
                
                setTimeout(() => {
                    historyPanel.style.transition = 'all 0.8s ease-out';
                    historyPanel.style.opacity = '1';
                    historyPanel.style.transform = 'translateX(0)';
                }, 200);
            }, 100);
        }
    }

    // Form validation
    initFormValidation() {
        // Add required indicators to labels
        const requiredFields = ['metalType', 'productionRoute', 'endOfLife'];
        requiredFields.forEach(fieldId => {
            const label = document.querySelector(`label[for="${fieldId}"]`);
            if (label && !label.classList.contains('required')) {
                label.classList.add('required');
            }
        });
    }

    // Validate individual field
    validateField(event) {
        const field = event.target;
        const value = field.value.trim();
        const fieldName = field.id;

        // Clear previous validation
        this.clearFieldErrors(event);

        let isValid = true;
        let errorMessage = '';

        // Validation rules
        switch (fieldName) {
            case 'metalType':
            case 'productionRoute':
            case 'endOfLife':
                if (!value) {
                    isValid = false;
                    errorMessage = 'This field is required';
                }
                break;
            
            case 'energyUse':
                if (value && (isNaN(value) || parseFloat(value) < 0)) {
                    isValid = false;
                    errorMessage = 'Energy use must be a positive number';
                }
                break;
            
            case 'transportDistance':
                if (value && (isNaN(value) || parseFloat(value) < 0)) {
                    isValid = false;
                    errorMessage = 'Transport distance must be a positive number';
                }
                break;
        }

        // Apply validation styles
        if (isValid) {
            field.classList.add('success');
            field.classList.remove('error');
            this.showFieldFeedback(field, 'Looks good!', 'valid');
        } else {
            field.classList.add('error');
            field.classList.remove('success');
            this.showFieldFeedback(field, errorMessage, 'invalid');
        }

        return isValid;
    }

    // Clear field errors
    clearFieldErrors(event) {
        const field = event.target;
        field.classList.remove('error', 'success');
        
        // Remove existing feedback
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback, .valid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
    }

    // Show field validation feedback
    showFieldFeedback(field, message, type) {
        // Remove existing feedback
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback, .valid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }

        // Create new feedback element
        const feedback = document.createElement('div');
        feedback.className = type === 'valid' ? 'valid-feedback' : 'invalid-feedback';
        feedback.textContent = message;
        feedback.style.display = 'block';
        
        field.parentNode.appendChild(feedback);
    }

    // Auto-save form data to localStorage
    autoSaveFormData() {
        const formData = {
            metalType: document.getElementById('metalType')?.value || '',
            productionRoute: document.getElementById('productionRoute')?.value || '',
            energyUse: document.getElementById('energyUse')?.value || '',
            transportDistance: document.getElementById('transportDistance')?.value || '',
            endOfLife: document.getElementById('endOfLife')?.value || '',
            timestamp: Date.now()
        };
        
        localStorage.setItem('lca_form_draft', JSON.stringify(formData));
    }

    // Load saved form data from localStorage
    loadSavedFormData() {
        try {
            const saved = localStorage.getItem('lca_form_draft');
            if (saved) {
                const data = JSON.parse(saved);
                // Only load if saved within last 24 hours
                if (Date.now() - data.timestamp < 24 * 60 * 60 * 1000) {
                    Object.keys(data).forEach(key => {
                        if (key !== 'timestamp') {
                            const field = document.getElementById(key);
                            if (field && data[key]) {
                                field.value = data[key];
                            }
                        }
                    });
                }
            }
        } catch (error) {
            console.warn('Could not load saved form data:', error);
        }
    }

    // Handle form submission with enhanced feedback
    async handleFormSubmit(event) {
        event.preventDefault();
        
        if (this.isLoading) return;
        
        // Validate all fields
        const formFields = document.querySelectorAll('.form-control');
        let allValid = true;
        
        formFields.forEach(field => {
            const mockEvent = { target: field };
            if (!this.validateField(mockEvent) && field.hasAttribute('required')) {
                allValid = false;
            }
        });

        if (!allValid) {
            this.showNotification('Please correct the errors in the form', 'error');
            return;
        }

        this.isLoading = true;
        this.showEnhancedLoading();
        
        // Collect form data
        const formData = {
            metalType: document.getElementById('metalType').value,
            productionRoute: document.getElementById('productionRoute').value,
            energyUse: parseFloat(document.getElementById('energyUse').value) || null,
            transportDistance: parseFloat(document.getElementById('transportDistance').value) || null,
            endOfLife: document.getElementById('endOfLife').value
        };

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.currentResults = data;
                await this.displayResultsWithAnimation(data);
                this.saveToHistory(formData, data);
                
                // Clear auto-saved draft
                localStorage.removeItem('lca_form_draft');
                
                this.showNotification('LCA calculation completed successfully!', 'success');
            } else {
                this.showError('Calculation error: ' + data.error);
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.hideLoading();
            this.isLoading = false;
        }
    }

    // Enhanced loading display
    showEnhancedLoading() {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.innerHTML = `
                <div class="loading-spinner"></div>
                <p>Processing your LCA calculation...</p>
                <div class="loading-progress">
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                    <p class="progress-text">Analyzing environmental impact...</p>
                </div>
            `;
            loadingElement.classList.add('show');
            
            // Animate progress bar
            this.animateProgress();
        }
        
        // Hide results and errors
        document.getElementById('results')?.classList.remove('show');
        document.getElementById('error')?.classList.remove('show');
    }

    // Animate loading progress
    animateProgress() {
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        if (!progressFill || !progressText) return;

        const steps = [
            'Analyzing material properties...',
            'Calculating energy requirements...',
            'Processing transportation impact...',
            'Evaluating end-of-life scenarios...',
            'Generating circular economy comparison...',
            'Finalizing results...'
        ];

        let currentStep = 0;
        const interval = setInterval(() => {
            if (currentStep < steps.length && this.isLoading) {
                progressFill.style.width = `${(currentStep + 1) * (100 / steps.length)}%`;
                progressText.textContent = steps[currentStep];
                currentStep++;
            } else {
                clearInterval(interval);
            }
        }, 800);
    }

    // Hide loading
    hideLoading() {
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.classList.remove('show');
        }
    }

    // Display results with smooth animation
    async displayResultsWithAnimation(data) {
        // Display enhanced parameters
        const paramsList = document.getElementById('paramsList');
        if (paramsList) {
            paramsList.innerHTML = Object.entries(data.enhanced_data)
                .map(([key, value]) => `<p><strong>${key}:</strong> ${value}</p>`)
                .join('');
        }
        
        // Display comparison table with animation
        const tableBody = document.getElementById('comparisonTableBody');
        if (tableBody) {
            tableBody.innerHTML = '';
            
            data.results.pathways.forEach((pathway, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${pathway.name}</td>
                    <td>${pathway.co2_equivalent.toFixed(2)}</td>
                    <td>${pathway.recycled_content.toFixed(1)}</td>
                    <td>${pathway.reuse_potential.toFixed(1)}</td>
                `;
                row.style.opacity = '0';
                row.style.transform = 'translateY(20px)';
                tableBody.appendChild(row);
                
                // Animate row appearance
                setTimeout(() => {
                    row.style.transition = 'all 0.5s ease-out';
                    row.style.opacity = '1';
                    row.style.transform = 'translateY(0)';
                }, index * 200);
            });
        }
        
        // Create enhanced chart
        setTimeout(() => {
            this.drawEnhancedChart(data.results.pathways);
        }, 600);
        
        // Show results container
        const resultsElement = document.getElementById('results');
        if (resultsElement) {
            resultsElement.classList.add('show');
            resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Enhanced chart drawing with animations
    drawEnhancedChart(pathways) {
        const canvas = document.getElementById('impactChart');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        canvas.width = 800;
        canvas.height = 400;
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Chart properties
        const margin = 80;
        const chartWidth = canvas.width - 2 * margin;
        const chartHeight = canvas.height - 2 * margin;
        const barWidth = chartWidth / pathways.length * 0.6;
        const maxValue = Math.max(...pathways.map(p => p.co2_equivalent));
        
        // Draw background grid
        this.drawChartGrid(ctx, margin, chartWidth, chartHeight);
        
        // Draw bars with animation
        pathways.forEach((pathway, index) => {
            const x = margin + (index * chartWidth / pathways.length) + (chartWidth / pathways.length - barWidth) / 2;
            const barHeight = (pathway.co2_equivalent / maxValue) * chartHeight;
            const y = margin + chartHeight - barHeight;
            
            // Color scheme
            const color = pathway.name.includes('Circular') 
                ? 'linear-gradient(135deg, #20c997, #20c997)' 
                : 'linear-gradient(135deg, #10cf23ff, #29ec36ff)';
            
            // Animate bar growth
            this.animateBar(ctx, x, margin + chartHeight, barWidth, barHeight, color, index * 300);
            
            // Draw labels
            setTimeout(() => {
                this.drawBarLabels(ctx, x, y, barWidth, barHeight, pathway, margin + chartHeight);
            }, index * 300 + 300);
        });
        
        // Draw chart title
        ctx.fillStyle = '#2c5aa0';
        ctx.font = 'bold 24px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText('Environmental Impact Comparison', canvas.width / 2, 40);
        
        // Draw axis labels
        ctx.font = '14px Segoe UI';
        ctx.fillStyle = '#6c757d';
        ctx.textAlign = 'center';
        ctx.fillText('Production Pathways', canvas.width / 2, canvas.height - 20);
        
        // Y-axis label
        ctx.save();
        ctx.translate(20, canvas.height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText('CO₂ Equivalent (kg CO₂/kg metal)', 0, 0);
        ctx.restore();
    }

    // Draw chart grid
    drawChartGrid(ctx, margin, chartWidth, chartHeight) {
        ctx.strokeStyle = '#efece9ff';
        ctx.lineWidth = 1;
        
        // Horizontal grid lines
        for (let i = 0; i <= 5; i++) {
            const y = margin + (chartHeight / 5) * i;
            ctx.beginPath();
            ctx.moveTo(margin, y);
            ctx.lineTo(margin + chartWidth, y);
            ctx.stroke();
        }
        
        // Vertical grid lines
        for (let i = 0; i <= 4; i++) {
            const x = margin + (chartWidth / 4) * i;
            ctx.beginPath();
            ctx.moveTo(x, margin);
            ctx.lineTo(x, margin + chartHeight);
            ctx.stroke();
        }
    }

    // Animate bar growth
    animateBar(ctx, x, baseY, width, targetHeight, color, delay) {
        setTimeout(() => {
            let currentHeight = 0;
            const increment = targetHeight / 20;
            
            const animate = () => {
                if (currentHeight < targetHeight) {
                    currentHeight += increment;
                    
                    // Clear previous bar
                    ctx.clearRect(x - 1, baseY - targetHeight - 1, width + 2, targetHeight + 2);
                    
                    // Draw current bar
                    const gradient = ctx.createLinearGradient(x, baseY - currentHeight, x, baseY);
                    if (color.includes('28a745')) {
                        gradient.addColorStop(0, '#28a745');
                        gradient.addColorStop(1, '#20c997');
                    } else {
                        gradient.addColorStop(0, '#dc5135b9');
                        gradient.addColorStop(1, '#e85d75');
                    }
                    
                    ctx.fillStyle = gradient;
                    ctx.fillRect(x, baseY - currentHeight, width, currentHeight);
                    
                    // Add shadow
                    ctx.shadowColor = 'rgba(0,0,0,0.2)';
                    ctx.shadowBlur = 4;
                    ctx.shadowOffsetY = 2;
                    
                    requestAnimationFrame(animate);
                } else {
                    // Draw final bar with border
                    ctx.strokeStyle = '#c46161ff';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, baseY - targetHeight, width, targetHeight);
                    ctx.shadowColor = 'transparent';
                }
            };
            
            animate();
        }, delay);
    }

    // Draw bar labels
    drawBarLabels(ctx, x, y, width, height, pathway, baseY) {
        ctx.fillStyle = '#343a40';
        ctx.font = '12px Segoe UI';
        ctx.textAlign = 'center';
        
        // Pathway name
        const pathwayName = pathway.name.replace(' Economy', '');
        ctx.fillText(pathwayName, x + width / 2, baseY + 20);
        
        // CO2 value
        ctx.fillStyle = '#ffffffff';
        ctx.font = 'bold 14px Segoe UI';
        ctx.fillText(
            `${pathway.co2_equivalent.toFixed(1)} kg CO₂`, 
            x + width / 2, 
            y + height / 2 + 5
        );
    }

    // Enhanced notification system
    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: '✓',
            error: '✕',
            info: 'ℹ',
            warning: '⚠'
        };
        
        notification.innerHTML = `
            <span class="notification-icon">${icons[type] || icons.info}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentNode.remove()">×</button>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${this.getNotificationColor(type)};
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            transform: translateX(100%);
            transition: transform 0.3s ease-out;
            max-width: 350px;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        // Auto remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, duration);
    }

    // Get notification color
    getNotificationColor(type) {
        const colors = {
            success: 'linear-gradient(135deg, #28a745, #20c997)',
            error: 'linear-gradient(135deg, #dc3545, #e85d75)',
            info: 'linear-gradient(135deg, #17a2b8, #20c997)',
            warning: 'linear-gradient(135deg, #ffc107, #fd7e14)'
        };
        return colors[type] || colors.info;
    }

    // Show error with animation
    showError(message) {
        const errorDiv = document.getElementById('error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }
        this.showNotification(message, 'error');
    }

    // History management methods (enhanced versions)
    saveToHistory(inputData, resultData) {
        let history = this.getHistoryFromStorage();
        
        const calculationId = Date.now();
        const historyItem = {
            id: calculationId,
            calculation_id: calculationId.toString(),
            timestamp: new Date().toISOString(),
            input: inputData,
            results: resultData,
            pdf_metadata: null
        };
        
        // Store calculation ID in current results
        if (this.currentResults) {
            this.currentResults.calculation_id = calculationId.toString();
        }
        
        history.unshift(historyItem);
        
        if (history.length > this.MAX_HISTORY_ITEMS) {
            history = history.slice(0, this.MAX_HISTORY_ITEMS);
        }
        
        localStorage.setItem(this.HISTORY_KEY, JSON.stringify(history));
        this.displayHistoryWithAnimation();
    }

    // Display history with animations
    displayHistoryWithAnimation() {
        const history = this.getHistoryFromStorage();
        const container = document.getElementById('historyContainer');
        
        if (!container) return;
        
        if (history.length === 0) {
            container.innerHTML = '<div class="no-history">No previous calculations found</div>';
            return;
        }
        
        const historyHTML = history.map((item, index) => {
            const date = new Date(item.timestamp).toLocaleDateString();
            const time = new Date(item.timestamp).toLocaleTimeString();
            
            const conventional = item.results.results.pathways.find(p => p.name.includes('Conventional'));
            const circular = item.results.results.pathways.find(p => p.name.includes('Circular'));
            
            const pdfSection = item.pdf_metadata ? `
                <div class="pdf-section">
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 12px;">
                        <span style="color: #007bff; font-weight: bold;">📄 PDF Available</span>
                        <button onclick="app.downloadPDF('${item.pdf_metadata.filename}')" 
                                class="btn btn-primary btn-sm">
                            Download
                        </button>
                        <span style="color: #6c757d;">${(item.pdf_metadata.file_size / 1024).toFixed(1)} KB</span>
                    </div>
                </div>
            ` : '';
            
            return `
                <div class="history-item" onclick="app.loadHistoryItem(${item.id})" style="opacity: 0; transform: translateY(20px);">
                    <div class="history-item-header">
                        <span class="history-date">${date} ${time}</span>
                        <button class="delete-history-item" onclick="event.stopPropagation(); app.deleteHistoryItem(${item.id})">✕</button>
                    </div>
                    <div class="history-details">
                        <div><strong>${item.input.metalType.charAt(0).toUpperCase() + item.input.metalType.slice(1)}</strong> - ${item.input.productionRoute.charAt(0).toUpperCase() + item.input.productionRoute.slice(1)}</div>
                        <div>End-of-life: ${item.input.endOfLife.charAt(0).toUpperCase() + item.input.endOfLife.slice(1)}</div>
                        ${item.input.energyUse ? `<div>Energy: ${item.input.energyUse.toFixed(1)} kWh/kg</div>` : ''}
                        ${item.input.transportDistance ? `<div>Transport: ${item.input.transportDistance.toFixed(1)} km</div>` : ''}
                    </div>
                    <div class="history-results">
                        <div>Conventional: <span class="co2-conventional">${conventional ? conventional.co2_equivalent.toFixed(2) : 'N/A'} kg CO₂</span></div>
                        <div>Circular: <span class="co2-circular">${circular ? circular.co2_equivalent.toFixed(2) : 'N/A'} kg CO₂</span></div>
                    </div>
                    ${pdfSection}
                </div>
            `;
        }).join('');
        
        container.innerHTML = historyHTML;
        
        // Animate items in
        const historyItems = container.querySelectorAll('.history-item');
        historyItems.forEach((item, index) => {
            setTimeout(() => {
                item.style.transition = 'all 0.5s ease-out';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // Load history from storage
    loadHistoryFromStorage() {
        this.displayHistoryWithAnimation();
    }

    // Get history from storage
    getHistoryFromStorage() {
        try {
            const stored = localStorage.getItem(this.HISTORY_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error reading history:', error);
            return [];
        }
    }

    // Load history item
    loadHistoryItem(itemId) {
        const history = this.getHistoryFromStorage();
        const item = history.find(h => h.id === itemId);
        
        if (!item) {
            this.showNotification('History item not found', 'error');
            return;
        }
        
        // Fill form with historical data
        Object.keys(item.input).forEach(key => {
            const field = document.getElementById(key);
            if (field) {
                field.value = item.input[key] || '';
            }
        });
        
        // Display the results
        this.currentResults = item.results;
        this.displayResultsWithAnimation(item.results);
        
        this.showNotification('Historical calculation loaded', 'success');
    }

    // Delete history item
    deleteHistoryItem(itemId) {
        if (!confirm('Are you sure you want to delete this calculation?')) {
            return;
        }
        
        let history = this.getHistoryFromStorage();
        history = history.filter(item => item.id !== itemId);
        
        localStorage.setItem(this.HISTORY_KEY, JSON.stringify(history));
        this.displayHistoryWithAnimation();
        
        this.showNotification('Calculation deleted', 'info');
    }

    // Clear all history
    clearAllHistory() {
        if (!confirm('Are you sure you want to clear all calculation history? This cannot be undone.')) {
            return;
        }
        
        localStorage.removeItem(this.HISTORY_KEY);
        this.displayHistoryWithAnimation();
        
        this.showNotification('All history cleared', 'info');
    }

    // Start new LCA
    startNewLCA() {
        this.clearForm();
        
        // Hide results and errors
        document.getElementById('results')?.classList.remove('show');
        document.getElementById('error')?.classList.remove('show');
        document.getElementById('loading')?.classList.remove('show');
        
        this.currentResults = null;
        
        // Scroll to top with animation
        document.querySelector('.container h1').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        // Focus first field
        setTimeout(() => {
            const firstField = document.getElementById('metalType');
            if (firstField) {
                firstField.focus();
            }
        }, 500);
        
        this.showNotification('Ready for new LCA calculation!', 'success');
    }

    // Clear form
    clearForm() {
        const formFields = document.querySelectorAll('.form-control');
        formFields.forEach(field => {
            field.value = '';
            field.classList.remove('error', 'success');
        });
        
        // Remove validation feedback
        const feedbacks = document.querySelectorAll('.invalid-feedback, .valid-feedback');
        feedbacks.forEach(feedback => feedback.remove());
        
        // Clear auto-saved draft
        localStorage.removeItem('lca_form_draft');
    }

    // PDF generation
    async generatePDFReport() {
        if (!this.currentResults) {
            this.showNotification('No results to generate report', 'warning');
            return;
        }
        
        const requestData = {
            ...this.currentResults,
            calculation_id: this.currentResults.calculation_id || Date.now().toString()
        };
        
        try {
            this.showNotification('Generating PDF report...', 'info');
            
            const response = await fetch('/generate_report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentResults.pdf_metadata = data.pdf_metadata;
                this.updateHistoryWithPDF(requestData.calculation_id || Date.now(), data.pdf_metadata);
                
                // Trigger download
                const a = document.createElement('a');
                a.href = data.download_url;
                a.download = data.pdf_metadata.filename;
                a.click();
                
                this.showNotification('PDF report generated and downloaded!', 'success');
            } else {
                this.showNotification('Failed to generate PDF: ' + data.error, 'error');
            }
        } catch (error) {
            this.showNotification('Error generating PDF: ' + error.message, 'error');
        }
    }

    // Update history with PDF metadata
    updateHistoryWithPDF(calculationId, pdfMetadata) {
        let history = this.getHistoryFromStorage();
        
        const historyItem = history.find(item => 
            item.calculation_id === calculationId.toString() || 
            item.id.toString() === calculationId.toString()
        );
        
        if (historyItem) {
            historyItem.pdf_metadata = pdfMetadata;
            localStorage.setItem(this.HISTORY_KEY, JSON.stringify(history));
            this.displayHistoryWithAnimation();
        }
    }

    // Download PDF
    downloadPDF(filename) {
        const downloadUrl = `/download_pdf/${filename}`;
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        a.click();
        
        this.showNotification('PDF download started', 'success');
    }
}

// Global functions for backward compatibility
let app;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    app = new LCAApp();
});

// Global function wrappers
function startNewLCA() {
    app?.startNewLCA();
}

function clearAllHistory() {
    app?.clearAllHistory();
}

function generatePDFReport() {
    app?.generatePDFReport();
}

function loadHistoryItem(itemId) {
    app?.loadHistoryItem(itemId);
}

function deleteHistoryItem(itemId) {
    app?.deleteHistoryItem(itemId);
}

function downloadPDF(filename) {
    app?.downloadPDF(filename);
}

// Add CSS for loading progress and notifications dynamically
const additionalCSS = `
    .loading-progress {
        margin-top: 20px;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }

    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 10px;
    }

    .progress-fill {
        width: 0%;
        height: 100%;
        background: linear-gradient(90deg, #2c5aa0, #4a7bc8);
        transition: width 0.8s ease-out;
    }

    .progress-text {
        text-align: center;
        font-size: 14px;
        color: #6c757d;
        font-style: italic;
        margin: 0;
    }

    .notification {
        font-family: var(--font-family-primary, 'Segoe UI', sans-serif);
        font-size: 14px;
    }

    .notification-close {
        background: none;
        border: none;
        color: rgba(255,255,255,0.8);
        cursor: pointer;
        font-size: 18px;
        padding: 0;
        margin-left: 10px;
    }

    .notification-close:hover {
        color: white;
    }
`;

// Inject additional CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalCSS;
document.head.appendChild(styleSheet);
