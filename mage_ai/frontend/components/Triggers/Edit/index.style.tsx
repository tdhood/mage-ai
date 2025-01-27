import styled from 'styled-components';

import dark from '@oracle/styles/themes/dark';
import { BORDER_RADIUS, BORDER_RADIUS_LARGE } from '@oracle/styles/units/borders';
import { PADDING, PADDING_UNITS, UNIT } from '@oracle/styles/units/spacing';
import { transition } from '@oracle/styles/mixins';

type CardProps = {
  selected?: boolean;
};

export const CardStyle = styled.div<CardProps>`
  border-radius: ${BORDER_RADIUS_LARGE}px;
  border-style: solid;
  border-width: 2px;
  height: ${14 * UNIT}px;
  margin-right: ${PADDING_UNITS * UNIT}px;
  padding: ${PADDING_UNITS * UNIT}px;
  width: ${40 * UNIT}px;


  ${props => !props.selected && `
    border-color: ${(props.theme.borders || dark.borders).light};
  `}

  ${props => props.selected && `
    border-color: ${(props.theme.interactive || dark.interactive).linkPrimary};
  `}
`;

export const DateSelectionContainer = styled.div`
  border-radius: ${BORDER_RADIUS}px;
  padding: ${PADDING}px;

  ${props => `
    background-color: ${(props.theme.interactive || dark.interactive).defaultBackground};
  `}
`;
