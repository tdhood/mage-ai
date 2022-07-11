export enum FileExtensionEnum {
  PY = 'py',
  TXT = 'txt',
}

export default interface FileType {
  children: FileType[];
  content?: string;
  disabled?: boolean;
  name: string;
  parent?: FileType;
  path?: string;
}

export const FOLDER_NAME_PIPELINES = 'pipelines';
export const FILE_EXTENSION_TO_LANGUAGE_MAPPING = {
  [FileExtensionEnum.PY]: 'python',
  [FileExtensionEnum.TXT]: 'text',
};