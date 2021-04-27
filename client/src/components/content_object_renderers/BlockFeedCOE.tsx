import React, { CSSProperties, useContext } from 'react';
import { Col, Container, Form, Row } from 'react-bootstrap';
import { ContentTreeAddIdContext, ContentTreeContext } from '../../contexts';
import {
    Block,
    BlockFeed,
    BlockType,
    ColumnsBlock,
    ImageBlock,
    RichTextBlock
} from '../../types/content_objects/blocks';
import { Popover, SvgIconTypeMap } from '@material-ui/core';
import TextFieldsIcon from '@material-ui/icons/TextFields';
import ImageIcon from '@material-ui/icons/Image';
import FormatAlignLeftIcon from '@material-ui/icons/FormatAlignLeft';
import VerticalSplitIcon from '@material-ui/icons/VerticalSplit';

import SettingsIcon from '@material-ui/icons/Settings';
import CancelIcon from '@material-ui/icons/Cancel';
import AddCircleSharpIcon from '@material-ui/icons/AddCircleSharp';

import FLargeIconButton from '../f-styled/buttons/FLargeIconButton';
import { OverridableComponent } from '@material-ui/core/OverridableComponent';
import BlockCOR from './blocks/BlockCOR';
import './BlockFeedCOE.scss';
import ColumnsBlockCOR from './blocks/ColumnsBlockCOR';

/**
 * Array of available blocks in block chooser popup.
 */
const blockIcons: { blockType: BlockType, text: string, icon: OverridableComponent<SvgIconTypeMap<{}, 'svg'>>}[] = [
    {
        blockType: 'heading',
        text: 'Heading',
        icon: TextFieldsIcon
    },
    {
        blockType: 'bodyText',
        text: 'Text',
        icon: FormatAlignLeftIcon
    },
    {
        blockType: 'image',
        text: 'Image',
        icon: ImageIcon
    },
    {
        blockType: 'columns',
        text: 'Columns',
        icon: VerticalSplitIcon
    }
];

/**
 * Definition of default blocks used for different block types.
 */
const defaultBlocks: {[key in BlockType]: Block} = {
    heading: {
        id: -1,
        detailUrl: '',
        dbType: 'text',
        attributes: {
            blockType: 'heading',
            richTextEditorType: 'only-headings'
        },
        text: '<h3></h3>'
    } as RichTextBlock,
    bodyText: {
        id: -1,
        detailUrl: '',
        dbType: 'text',
        attributes: {
            blockType: 'bodyText',
            richTextEditorType: 'body-text'
        },
        text: '<p></p>'
    } as RichTextBlock,
    image: {
        id: -1,
        detailUrl: '',
        dbType: 'image',
        attributes: {
            blockType: 'image',
            alignment: 'center',
            width: '100%'
        },
        image: {
            id: -1,
            detailUrl: '',
            href: ''
        }
    } as ImageBlock,
    columns: {
        id: -1,
        detailUrl: '',
        dbType: 'dict',
        attributes: {
            blockType: 'columns',
            split: 6
        },
        items: {
            left: {
                id: -1,
                detailUrl: '',
                dbType: 'list',
                attributes: {},
                items: []
            },
            right: {
                id: -1,
                detailUrl: '',
                dbType: 'list',
                attributes: {},
                items: []
            }
        }
    } as ColumnsBlock
};

type AddBlockButtonProps = {
    index: number,
    content: BlockFeed,
    style?: CSSProperties
}

/**
 * Adds a block *after* index in the list of children of FeedCO.
 * @param index The index in FeedCO.items to add blick after
 * @param ListCO The CO containing list of feed as items.
 * @constructor
 */
function AddBlockButton({ index, content, style }: AddBlockButtonProps) {
    const dispatch = useContext(ContentTreeContext);
    const addIdState = useContext(ContentTreeAddIdContext);

    function add(blockType: BlockType) {
        const newBlock = defaultBlocks[blockType];
        newBlock.id = addIdState.id;
        if (blockType === 'columns') {
            (newBlock as ColumnsBlock).items.left.id = addIdState.id - 1;
            (newBlock as ColumnsBlock).items.right.id = addIdState.id - 2;
            addIdState.decrementHook({ id: addIdState.id - 3 });
        } else {
            addIdState.decrementHook({ id: addIdState.id - 1 });
        }

        const newContent = { ...content };
        const items = content.items.slice(0, index + 1);
        items.push(newBlock);
        newContent.items = items.concat(content.items.slice(index + 1, undefined)) as Block[];

        dispatch({ id: content.id, value: newContent });
    }

    const [anchorEl, setAnchorEl] = React.useState<EventTarget & Element | null>(null);
    function onClick(event: React.MouseEvent) {
        setAnchorEl(event.currentTarget);
    }
    const handleClose = () => {
        setAnchorEl(null);
    };
    const open = Boolean(anchorEl);
    const popoverId = 'popover-' + index;

    return (
        <>
            <div className='d-flex justify-content-center w-100 show-children-on-hover' style={{ height: '30px' }}>
                <AddCircleSharpIcon
                    className='show-on-parent-hover text-center'
                    aria-describedby={popoverId}
                    style={style}
                    onClick={onClick}
                />
            </div>
            <Popover
                id={popoverId}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'center'
                }}
                transformOrigin={{
                    vertical: 'bottom',
                    horizontal: 'center'
                }}
                className='zoom-xs-10 zoom-xl-8'
            >
                <Container>
                    <Row>
                        {blockIcons.map((item, index) => {
                            return (
                                <Col key={index}>
                                    <FLargeIconButton text={item.text} Icon={item.icon} onClick={() => add(item.blockType)}/>
                                </Col>
                            );
                        })}
                    </Row>
                </Container>
            </Popover>
        </>
    );
}

type RemoveBlockButtonProps = {
    index: number,
    content: BlockFeed,
    className?: string,
    style?: CSSProperties
}

/**
 * Removes the block at index in the list of children of `content`.
 * @param index Index to remove at
 * @param content ContentList containing the list from which to remove the item
 * @param className Extra classNames on the <i> tag
 * @param style Extra styling added to the <i> tag
 * @constructor
 */
function RemoveBlockButton({ index, content, className, style }: RemoveBlockButtonProps) {
    const dispatch = useContext(ContentTreeContext);

    function deleteBlock(index: number) {
        const newCOFeed = {
            ...content
        };
        const items = content.items.slice(0, index);
        newCOFeed.items = items.concat(content.items.slice(index + 1, undefined)) as Block[];

        dispatch({ id: content.id, value: newCOFeed });
    }

    return (
        <CancelIcon
            className={'position-absolute show-on-parent-hover ' + className ?? ''}
            onClick={() => deleteBlock(index)}
            style={style}
        />
    );
}

type EditBlockButtonProps = {
    index: number,
    content: BlockFeed,
    style?: CSSProperties
}

/**
 * Edit the block at index in the list of children of `content`.
 * @param index Index to edit
 * @param content ContentList containing the list from which to edit the item
 * @param style Extra styling added to the <i> tag
 * @constructor
 */
function EditColumnsBlockButton({ index, content, style }: EditBlockButtonProps) {
    const dispatch = useContext(ContentTreeContext);

    function updateContent(split: number) {
        const newCOFeed = {
            ...content
        };
        // @ts-ignore
        (newCOFeed.items[index] as ColumnsBlock).attributes.split = split;
        dispatch({ id: content.id, value: newCOFeed });
    }

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        updateContent(parseInt(event.target.value, 10));
    };

    const [anchorEl, setAnchorEl] = React.useState<EventTarget & Element | null>(null);
    function onClick(event: React.MouseEvent) {
        setAnchorEl(event.currentTarget);
    }
    const handleClose = () => {
        setAnchorEl(null);
    };
    const open = Boolean(anchorEl);
    const popoverId = 'popover-' + index;

    return (
        <>
            <SettingsIcon
                className='position-absolute show-on-parent-hover'
                aria-describedby={popoverId}
                style={style}
                onClick={onClick}
            />
            <Popover
                id={popoverId}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'center'
                }}
                transformOrigin={{
                    vertical: 'bottom',
                    horizontal: 'center'
                }}
                className='zoom-xs-10 zoom-xl-8'
            >
                <Container>
                    <Form>
                        <Form.Group controlId="formBasicRange">
                            <Form.Label>Column width (left column)</Form.Label>
                            <Form.Control type="range" min="1" max="11" step="1" onChange={handleChange} />
                        </Form.Group>
                    </Form>
                </Container>
            </Popover>
        </>
    );
}

export type BlockFeedCOEProps = {
    content: BlockFeed
}

/**
 * Component rendering a BlockFeed and allows for editing behaviour. Allows for adding blocks and removing blocks.
 * @param content The BlockFeed object to render and edit.
 * @constructor
 */
export default function BlockFeedCOE({ content }: BlockFeedCOEProps) {
    const iconSize = 30;

    return (
        <Col xs={12}>
            <Row className='soft-dashed-border-on-hover'>
                <AddBlockButton index={-1} content={content}
                    style={{
                        width: iconSize.toString() + 'px',
                        height: iconSize.toString() + 'px'
                    }}
                />
            </Row>
            {content.items.map((obj, index) => {
                return (
                    <>
                        <Row className='position-relative show-children-on-hover soft-dashed-border-on-hover'>
                            {obj.attributes.blockType === 'columns' &&
                                <EditColumnsBlockButton index={index} content={content}
                                    style={{
                                        width: iconSize.toString() + 'px',
                                        height: iconSize.toString() + 'px',
                                        right: (1.5 * iconSize / 2).toString() + 'px',
                                        top: '-' + (iconSize / 2).toString() + 'px'
                                    }}
                                />
                            }
                            <RemoveBlockButton index={index} content={content}
                                style={{
                                    width: iconSize.toString() + 'px',
                                    height: iconSize.toString() + 'px',
                                    right: '-' + (iconSize / 2).toString() + 'px',
                                    top: '-' + (iconSize / 2).toString() + 'px'
                                }}
                            />
                            <BlockCOR block={obj} />
                        </Row>
                        <Row className='soft-dashed-border-on-hover'>
                            <AddBlockButton index={index} content={content}
                                style={{
                                    width: iconSize.toString() + 'px',
                                    height: iconSize.toString() + 'px'
                                }}
                            />
                        </Row>
                    </>
                );
            })}
        </Col>
    );
}
