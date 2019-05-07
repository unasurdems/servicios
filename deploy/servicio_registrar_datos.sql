CREATE OR REPLACE FUNCTION public.servicio_registrar_datos(
    nombre_facturacion CHARACTER VARYING,
    ci_nit CHARACTER VARYING,
    ciudad CHARACTER VARYING,
    urbano_rural CHARACTER VARYING,
    depto CHARACTER VARYING,
    depto_id INTEGER,
    depto_descr CHARACTER VARYING,
    municipio CHARACTER VARYING,
    municipio_id_depto INTEGER,
    municipio_descr CHARACTER VARYING,
    municipio_id_provincia INTEGER,
    municipio_id_alcaldia INTEGER,
    municipio_dpa CHARACTER VARYING,
    dpa CHARACTER VARYING,
    zonauv CHARACTER VARYING,
    zonauv_codigo_zona CHARACTER VARYING,
    zonauv_descr CHARACTER VARYING,
    zonauv_cod_adm CHARACTER VARYING,
    marker CHARACTER VARYING,
    marker_id INTEGER,
    marker_position CHARACTER VARYING,
    marker_lat CHARACTER VARYING,
    marker_long CHARACTER VARYING,
    marker_visible CHARACTER VARYING,
    marker_visible2 CHARACTER VARYING,
    marker_drag CHARACTER VARYING,
    zona_barrio_uv_otro CHARACTER VARYING,
    calle_avenida CHARACTER VARYING,
    dir_referencial CHARACTER VARYING,
    numero CHARACTER VARYING,
    edificio CHARACTER VARYING,
    piso CHARACTER VARYING,
    departamento_local_oficina CHARACTER VARYING,
    longitud CHARACTER VARYING,
    latitud CHARACTER VARYING,
    usuario INTEGER
)
RETURNS response AS
$BODY$
/**
* Funcion: servicio_registrar_datos
* Author: Edwin Ajahuanca C.
* Descripcion: Esta funcion registra los datos enviados como: 
               departamentos, provincia, muncipio, zona, alcaldia, ubicacion(marker)
*
 */
DECLARE
    response RESPONSE;
BEGIN
    response.type := 'S';
    response.message := 'Registro realizado de manera exitosa';
    -- REALIZAR EL INSERT DE CADA TABLA CORRESPONDIENTE
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;