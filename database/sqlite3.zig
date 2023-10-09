const std = @import("std");

const c = @cImport({
    @cInclude("sqlite3.h");
});

var db_name: ?[*:0]const u8 = null;
var db: ?*c.sqlite3 = null;

const SQLError = error{ LoadFailed, UninitializeError, SQLiteBusy, SqlError };

pub fn load_db(_db_name: [*:0]const u8) c_int {
    // Open database
    const sqlFd = c.sqlite3_open(_db_name, &db);
    if (sqlFd != 0) {
        std.debug.print("Can't open database: {s}", .{_db_name});
        _ = c.sqlite3_close_v2(db);
        return -1;
    }
    _ = std.debug.print("Database {s} opened successfully.\n", .{_db_name});
    db_name = _db_name;
    return sqlFd;
}

pub fn close_db() !void {
    if (db) |_db| {
        switch (c.sqlite3_close_v2(_db)) {
            c.SQLITE_OK => {
                std.debug.print("Database {s} closed.\n", .{db_name orelse unreachable});
            },
            c.SQLITE_BUSY => {
                std.debug.print("SQL error: {s}\n", .{c.sqlite3_errmsg(db orelse null)});
                return SQLError.SQLiteBusy;
            },
            else => unreachable,
        }
    } else {
        return SQLError.UninitializeError;
    }
}

pub fn execute(query: [*:0]const u8) !void {
    if (db_name == null) {
        return SQLError.UninitializeError;
    }
    var stmt: ?*c.sqlite3_stmt = null;
    const prepare_result = c.sqlite3_prepare_v2(db, query, -1, &stmt, null);
    if (prepare_result != c.SQLITE_OK) {
        std.debug.print("SQL error: {s}\n", .{c.sqlite3_errmsg(db orelse null)});
        return SQLError.SqlError;
    }

    while (c.sqlite3_step(stmt) == c.SQLITE_ROW) {
        const id = c.sqlite3_column_int(stmt, 0);
        const name_ptr = c.sqlite3_column_text(stmt, 1);

        if (name_ptr == null) {
            std.debug.print("use the wrong mode\n", .{});
            return SQLError.SqlError;
        }

        std.debug.print("ID: {}, Name: {s}\n", .{ id, name_ptr });
    }
}
