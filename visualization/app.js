let trafficData = null;
        
        // 显示加载动画
        function showLoading() {
            document.getElementById('loading-container').style.display = 'flex';
            document.getElementById('main-content').style.display = 'none';
            document.getElementById('error-container').style.display = 'none';
        }
        
        // 隐藏加载动画
        function hideLoading() {
            document.getElementById('loading-container').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            document.getElementById('error-container').style.display = 'none';
        }
        
        // 显示错误页面
        function showError(message) {
            document.getElementById('loading-container').style.display = 'none';
            document.getElementById('main-content').style.display = 'none';
            document.getElementById('error-container').style.display = 'flex';
            document.getElementById('error-message').textContent = message;
        }
        
        showLoading();// DEBUG: mark script execution

        
        document.addEventListener('DOMContentLoaded', function() {
            fetch('data/traffic_data.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    trafficData = preprocessData(data);hideLoading();setTimeout(() => {
                        try {
                            initCharts();updateCharts();