var CONFIG = {

    PROJECT: '{{ config["PROJECT"] }}',
    COMPANY: '{{ config["COMPANY"] }}',

    EMAIL: '{{ config["EMAIL"] }}',
    GITHUB: '{{ config["GITHUB"] }}',
    WEBSITE: '{{ config["WEBSITE"] }}',
    LINKEDIN: '{{ config["LINKEDIN"] }}',

    ENDPOINT: '{{ url_for(request.endpoint) }}',
    SITEMAP: JSON.parse('{{ sitemap | tojson }}'),
    INPUTS: JSON.parse('{{ inputs | tojson }}'),
    OUTPUT: JSON.parse('{{ output | tojson }}'),

}
