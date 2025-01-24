{% macro example_macro_1(variable) %}
    {{ variable | int + 5 }}
{% endmacro %}