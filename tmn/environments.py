environments = {
    'mainnet': {
        'tomochain': {
            'BOOTNODES': (
                'enode://97f0ca95a653e3c44d5df2674e19e9324ea4bf4d47a46b1d8560f'
                '3ed4ea328f725acec3fcfcb37eb11706cf07da669e9688b091f1543f89b24'
                '25700a68bc8876@104.248.98.78:30301,enode://b72927f349f3a27b78'
                '9d0ca615ffe3526f361665b496c80e7cc19dace78bd94785fdadc270054ab'
                '727dbb172d9e3113694600dd31b2558dd77ad85a869032dea@188.166.207'
                '.189:30301,enode://c8f2f0643527d4efffb8cb10ef9b6da4310c5ac9f2'
                'e988a7f85363e81d42f1793f64a9aa127dbaff56b1e8011f90fe9ff57fa02'
                'a36f73220da5ff81d8b8df351@104.248.98.60:30301'
            ),
            'NETSTATS_HOST': 'stats.tomochain.com',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '88',
            'WS_SECRET': (
                'getty-site-pablo-auger-room-sos-blair-shin-whiz-delhi'
            )
        },
        'metrics': {
            'METRICS_ENDPOINT': 'https://metrics.tomochain.com'
        }
    },
    'testnet': {
        'tomochain': {
            'BOOTNODES': (
                'enode://4d3c2cc0ce7135c1778c6f1cfda623ab44b4b6db55289543d48ec'
                'fde7d7111fd420c42174a9f2fea511a04cf6eac4ec69b4456bfaaae0e5bd2'
                '36107d3172b013@52.221.28.223:30301,enode://298780104303fcdb37'
                'a84c5702ebd9ec660971629f68a933fd91f7350c54eea0e294b0857f1fd2e'
                '8dba2869fcc36b83e6de553c386cf4ff26f19672955d9f312@13.251.101.'
                '216:30301,enode://46dba3a8721c589bede3c134d755eb1a38ae7c5a4c6'
                '9249b8317c55adc8d46a369f98b06514ecec4b4ff150712085176818d18f5'
                '9a9e6311a52dbe68cff5b2ae@13.250.94.232:30301'
            ),
            'NETSTATS_HOST': 'stats.testnet.tomochain.com',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '89',
            'WS_SECRET': (
                'anna-coal-flee-carrie-zip-hhhh-tarry-laue-felon-rhine'
            )
        },
        'metrics': {
            'METRICS_ENDPOINT': 'https://metrics.testnet.tomochain.com'
        }
    },
    'devnet': {
        'tomochain': {
            'BOOTNODES': (
                'enode://5bec42d41c9eb291c1d20c9ac92bd9c86a4954189b6592b0833e5'
                'c28e389b59e3992efed119a2782d9b95ba7aa78e7f71813067cd6734fadff'
                '322f7dd6fc3b3c@104.248.99.234:30301,enode://89028bc15e9dda643'
                'bc4b9a1a6352896dd3bce7411543b0b160a9eb95093ddbe1f5eda5999e38a'
                '4874bfa6a00fb3526cc2fb9b4feb2a3f7cc80ef8016e05c493@104.248.99'
                '.235:30301,enode://ea8f1eb1a2a695960bfa6df52094c635e173c65e5f'
                'c120501672c0d21900d826d6c1c5a07d64ad36509ec5e7306d7a2c3398398'
                'f34f3e279b91c487c2b3a9537@104.248.99.233:30301'
            ),

            'NETSTATS_HOST': 'stats.devnet.tomochain.com',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '90',
            'WS_SECRET': (
                'torn-fcc-caper-drool-jelly-zip-din-fraud-rater-darn'
            )
        },
        'metrics': {
            'METRICS_ENDPOINT': 'https://metrics.devnet.tomochain.com'
        }
    }
}
