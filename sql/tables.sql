create table devices (
    device_id varchar(12),
    device_name varchar(64),
    device_type varchar(32),
    primary key(device_id)
);

create table temperature_humidity_logs (
    device_id varchar(12),
    log_time timestamptz,
    temperature float,
    humidity float,
    primary key(device_id, log_time),
    foreign key(device_id) references devices(device_id)
);
