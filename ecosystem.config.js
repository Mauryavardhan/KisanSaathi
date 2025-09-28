module.exports = {
  apps: [{
    name: 'kisan-saathi-frontend',
    script: 'server.js',
    instances: process.env.NODE_ENV === 'production' ? 'max' : 1,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    // Logging
    log_file: './logs/app.log',
    error_file: './logs/error.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    
    // Memory management
    max_memory_restart: '1G',
    
    // Auto restart
    watch: false,
    ignore_watch: ['node_modules', 'logs', '.next'],
    
    // Health monitoring
    min_uptime: '10s',
    max_restarts: 10,
    
    // Environment specific settings
    node_args: process.env.NODE_ENV === 'production' ? '--max-old-space-size=2048' : '',
    
    // Graceful shutdown
    kill_timeout: 5000,
    wait_ready: true,
    listen_timeout: 10000,
    
    // Source maps (for better error tracking)
    source_map_support: true,
    
    // Merge logs
    merge_logs: true,
    
    // Time format
    time: true
  }]
}
