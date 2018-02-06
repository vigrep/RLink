"""
角色-权限
"""


# 权限
class Permission:
    BASIC = 0x01
    MANAGE_LINK = 0x02
    MANAGE_USER = 0x04
    MANAGE_CATEGORY = 0x08
    MANAGE_ROLE = 0x10
    MANAGE_PRIMARY = 0x20
    MANAGE_WORTHY = 0x40

    Permissions = {
        BASIC: "普通用户最基本操作",
        MANAGE_LINK: "链接表操作权限",
        MANAGE_USER: "用户表操作权限",
        MANAGE_CATEGORY: "类别表操作权限",
        MANAGE_ROLE: "角色表操作权限",
        MANAGE_PRIMARY: "首要推荐表操作权限",
        MANAGE_WORTHY: "推荐表操作权限",
    }

    # 接下来的：4个字节，每个字节八位，每一位置1代表一个权限，4位二进制表示1位16进制
    # 0x40
    # 0x80
    # 0x100
    # ...
    # 0x1000
    # ...
    # 0x10000
    # ...
    # 0x100000
    # ...
    # 0x1000000
    # ...
    # 0x10000000
    # GOD = 0x7fffffff      # 最大表示

    @staticmethod
    def get_permissions(only=None):
        """
        获取权限列表
        :param only: list类型，仅显示该列表中列出的权限
        :return: [{"permission_id": 0x01, "description": "权限描述信息"}, ....]
        """
        permission_list = list()
        for value, description in Permission.Permissions.items():
            if only is None or (isinstance(only, list) and value in only):
                permission_dict = {"permission_id": value, "description": description}
                permission_list.append(permission_dict)
        return permission_list

    @staticmethod
    def combine_permissions(permission_list):
        """
        将[0x01, 0x02...] 转换成 0x01 | 0x02 | ... 后的结果
        （将permission_list中数值进行或操作，得到最终的权限值)
        :param permission_list: 含有单独权限数值的列表
        :return:
        """
        if not isinstance(permission_list, list) or len(permission_list) == 0:
            return 0x00
        try:
            total = 0x00
            for permission in permission_list:
                if permission in Permission.Permissions:
                    total = total | permission
            return total
        except:
            return 0x00

    @staticmethod
    def split_permission(total_permission):
        """
        combine_permissions() 函数的逆操作
        :param total_permission:
        :return:
        """
        if not isinstance(total_permission, int):
            return []
        try:
            permissions_list = []
            for permission in Permission.Permissions:
                # 输出二进制
                # print('{0:b}'.format(permission))
                # print('{0:b}'.format(total_permission))
                # print('{0:b}'.format(permission & total_permission))
                if (permission & total_permission) == permission:
                    permissions_list.append(permission)
            return permissions_list
        except:
            return []

