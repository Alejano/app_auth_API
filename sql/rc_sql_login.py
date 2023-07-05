class SqlStrings():
    qry_login_pgsql =  \
    """
        select vp2.userid,vp2.personaid,vp2.perfilid perfil,p.nombre tmp_name,dc.email tmp_email,vp2.username,vp2.enable,
            vp2.createat
           from party.users vp2
           join party.personas p on p.personaid=vp2.personaid
            join party.datos_contacto dc on dc.personaid=vp2.personaid
        where vp2.username = '{}' and upper(vp2.password)='{}'
    """

    qry_login_funcion_pgsql =  \
    """
        select * from party.login('{}','{}');
    """

    qry_email_pgsql =  \
    """
            select vp2.userid,vp2.personaid,vp2.perfilid perfil,p.nombre tmp_name,dc.email tmp_email,vp2.username,vp2.enable,
            vp2.createat
           from party.users vp2
           join party.personas p on p.personaid=vp2.personaid
            join party.datos_contacto dc on dc.personaid=vp2.personaid
           where vp2.username = '{}'
    """

    qry_cambia_pass =  \
    """
            select * from party.reset_password({},{},'{}')
    """


# and vp2.enable=1




 