#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sm6225-common',
    'hardware/qcom-caf/sm6225',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


libs_add_vendor_suffix = (
    'vendor.qti.hardware.qccsyshal@1.0',
    'vendor.qti.hardware.qccsyshal@1.1',
    'vendor.qti.hardware.qccsyshal@1.2',
    'vendor.qti.hardware.qccvndhal@1.0',
    'vendor.qti.hardware.sigma_miracast@1.0',
    'vendor.qti.hardware.wifidisplaysession@1.0',
    'vendor.qti.imsrtpservice@3.0',
    'vendor.qti.imsrtpservice@3.1',
    'vendor.qti.diaghal@1.0',
    'com.qualcomm.qti.dpm.api@1.0',
)

libs_remove = (
    'libar-pal',
    'libar-acdb',
    'liblx-osal',
    'libats',
    'libagm',
    'libpalclient',
)


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    libs_add_vendor_suffix: lib_fixup_vendor_suffix,
    libs_remove: lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/bin/hw/android.hardware.security.keymint-service-qti', 'vendor/lib64/libqtikeymint.so'): blob_fixup()
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libinput_shim.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/etc/qcril_database/upgrade/other/0_initial_qcrilnr.sql': blob_fixup()
        .regex_replace(
            r'CREATE TABLE qcril_properties_table\s*\(\s*property TEXT PRIMARY KEY NOT NULL,\s*def_val TEXT,\s*value TEXT\s*\);',
            'CREATE TABLE qcril_properties_table (property TEXT,value TEXT, PRIMARY KEY(property));'
        ),
    'vendor/etc/qcril_database/upgrade/other/5_version_update_ecc_table_qcrilnr.sql': blob_fixup()
        .regex_replace( r'COMMIT TRANSACTION;\s*',''),
    'vendor/etc/qcril_database/upgrade/other/7_version_update_ecc_table.sql': blob_fixup()
        .regex_replace(
            r'(?m)^INSERT INTO qcril_emergency_source_hard_mcc_table',
            'INSERT OR REPLACE INTO qcril_emergency_source_hard_mcc_table'
        )
        .regex_replace(
             r'(?m)^INSERT INTO qcril_emergency_source_mcc_mnc_table',
            'INSERT OR REPLACE INTO qcril_emergency_source_mcc_mnc_table'
        ),
    'vendor/etc/qcril_database/upgrade/other/9_version_update_ecc_table.sql': blob_fixup()
        .regex_replace(
            r'(?m)^INSERT INTO qcril_emergency_source_hard_mcc_table',
            'INSERT OR REPLACE INTO qcril_emergency_source_hard_mcc_table'
        ),
    'vendor/etc/qcril_database/upgrade/other/15_version_update_ecc_table.sql': blob_fixup()
        .regex_replace(
            r"(INSERT INTO qcril_emergency_source_hard_mcc_table\b.*?where\s+MCC\s*=\s*'(\d+)'\s+AND\s+NUMBER\s*=\s*'(\d+)';)",
            r"INSERT OR REPLACE INTO qcril_emergency_source_hard_mcc_table (MCC, NUMBER) VALUES ('\2', '\3');"

        )
} # fmt: skip

module = ExtractUtilsModule(
    'sm6225-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
