import { BlockTypeEnum } from '@interfaces/BlockType';

export enum LogLevelEnum {
  CRITICAL = 'CRITICAL',
  DEBUG = 'DEBUG',
  ERROR = 'ERROR',
  EXCEPTION = 'EXCEPTION',
  INFO = 'INFO',
  LOG = 'LOG',
  WARNING = 'WARNING',
}

export const LOG_LEVELS = [
  LogLevelEnum.CRITICAL,
  LogLevelEnum.DEBUG,
  LogLevelEnum.ERROR,
  LogLevelEnum.EXCEPTION,
  LogLevelEnum.INFO,
  LogLevelEnum.LOG,
  LogLevelEnum.WARNING,
];

export interface LogDataType {
  block_run_id?: number;
  block_type?: BlockTypeEnum;
  block_uuid?: string;
  error?: string[];
  error_stack?: string[][];
  error_stacktrace: string;
  level: LogLevelEnum;
  message: string;
  pipeline_run_id?: number;
  pipeline_schedule_id?: number;
  pipeline_uuid?: string;
  timestamp: number;
  uuid: string;
}

export default interface LogType {
  content: string;
  createdAt?: string;
  data?: LogDataType;
  name: string;
  path: string;
}
